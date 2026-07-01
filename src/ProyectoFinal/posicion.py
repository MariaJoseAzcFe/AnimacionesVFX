"""
posicion.py

Algoritmos de interpolación

Autores: Josemi, Maria José, Juan Pablo


"""
import bpy
import math 
import importlib
import interpola;

from mathutils import Vector, Quaternion

AXIS_VECTORS = {
    'X': Vector((1, 0, 0)),
    'Y': Vector((0, 1, 0)),
    'Z': Vector((0, 0, 1)),
    '-X': Vector((-1, 0, 0)),
    '-Y': Vector((0, -1, 0)),
    '-Z': Vector((0, 0, -1)),
}

################### Funciones principales #####################

def get_keyframe_segment(keyframes, frm: float):
    """
    Función auxiliar para encontrar el segmento de keyframes
    que rodea al fotograma 'frm'.
    Devuelve una tupla (key_prev, key_next)
    """
    if not keyframes:
        return None
    keys_list = list(keyframes) 

    if frm <= keys_list[0].co[0]:
        return (keys_list[0], keys_list[0])
    
    if frm >= keys_list[-1].co[0]:
        return (keys_list[-1], keys_list[-1])
        
    key_prev = keys_list[0]
    for key_next in keys_list:
        if key_next.co[0] > frm:
            break
        key_prev = key_next

    return (key_prev, key_next)

def calcula_longitud_recorrida(obj):
    """
    Calcula la longitud acumulada de la curva frame a frame y guarda
    los datos en la propiedad 'distancia_recorrida'.
    """
    # Verificamos que haya animación
    if not obj.animation_data or not obj.animation_data.action:
        return 0.0

    start_frame = int(obj.animation_data.action.frame_range[0])
    end_frame = int(obj.animation_data.action.frame_range[1])
    
    # Limpiamos datos previos
    obj["distancia_recorrida"] = 0.0
    
    # 1. Posición inicial
    # IMPORTANTE: Usamos force_original=True para medir la geometría real
    # sin que nos afecte si el control de velocidad está activado o no.
    pos_prev = Vector((
        get_posicion(start_frame, obj, 0, force_original=True),
        get_posicion(start_frame, obj, 1, force_original=True),
        get_posicion(start_frame, obj, 2, force_original=True)
    ))
    
    dist_total = 0.0
    
    # Insertamos keyframe inicial
    obj.keyframe_insert(data_path='["distancia_recorrida"]', frame=start_frame)

    # 2. Bucle de medición
    for f in range(start_frame + 1, end_frame + 1):
        pos_curr = Vector((
            get_posicion(f, obj, 0, force_original=True),
            get_posicion(f, obj, 1, force_original=True),
            get_posicion(f, obj, 2, force_original=True)
        ))
        
        dist_paso = (pos_curr - pos_prev).length
        dist_total += dist_paso
        
        # Guardamos en la propiedad (Requisito del PDF )
        obj["distancia_recorrida"] = dist_total
        obj.keyframe_insert(data_path='["distancia_recorrida"]', frame=f)
        
        pos_prev = pos_curr

    # Interpolación Lineal para la distancia
    fcurve = obj.animation_data.action.fcurves.find('["distancia_recorrida"]')
    if fcurve:
        for kp in fcurve.keyframe_points:
            kp.interpolation = 'LINEAR'
            
    print(f"Longitud calculada: {dist_total}")
    return dist_total

def frame_desde_longitud(obj, dist_objetivo):
    """
    Recibe una distancia (metros) y devuelve el frame (con decimales)
    en el que se alcanza dicha distancia en la curva original.
    """
    # Buscamos la curva de datos que creamos en el paso anterior
    if not obj.animation_data or not obj.animation_data.action:
        return 0.0
        
    fcurve = obj.animation_data.action.fcurves.find('["distancia_recorrida"]')
    if not fcurve:
        return 0.0
    
    kps = fcurve.keyframe_points
    
    # 1. Búsqueda del intervalo 
    # Iteramos por los puntos guardados
    for i in range(len(kps) - 1):
        kp_prev = kps[i]
        kp_next = kps[i+1]
        
        val_prev = kp_prev.co[1] # Distancia en el punto i
        val_next = kp_next.co[1] # Distancia en el punto i+1
        
        # Verificamos si nuestra distancia objetivo está en este hueco
        if val_prev <= dist_objetivo <= val_next:
            # 2. Interpolación lineal para obtener el frame exacto 
            # Fórmula: t = t0 + (d - d0) / (d1 - d0) * (t1 - t0)
            
            rango_dist = val_next - val_prev
            if rango_dist == 0: 
                return kp_prev.co[0]
            
            porcentaje = (dist_objetivo - val_prev) / rango_dist
            frame_resultante = kp_prev.co[0] + porcentaje * (kp_next.co[0] - kp_prev.co[0])
            
            return frame_resultante
            
    # Si la distancia es mayor al total, devolvemos el último frame
    return kps[-1].co[0] 

def get_posicion(frm: float, obj, coord: int, force_original=False):
    """
    Función ÚNICA: Maneja la lógica de velocidad (P4) y la matemática (P3).
    """

    # --- PARTE 1: LÓGICA DE VELOCIDAD (REPARAMETRIZACIÓN) ---
    # Si el usuario quiere control de velocidad Y no estamos forzando la original
    if not force_original and getattr(obj, "use_speed_control", False):
        
        # 1. Obtener la distancia deseada
        try:
            # Intentamos leer la propiedad animada por el usuario
            dist_target = obj.distancia_deseada
        except AttributeError:
            # Fallback por si acaso
            dist_target = frm / 24.0

        # 2. Convertir Metros -> Frame "Virtual" (Usando tu función de búsqueda)
        frame_reparametrizado = frame_desde_longitud(obj, dist_target)

        # 3. RECURSIVIDAD SEGURA:
        # Llamamos a esta misma función pero activamos el "force_original=True".
        # Esto hace que en la siguiente vuelta salte este bloque 'if' y vaya directo
        # a la PARTE 2 (cálculo matemático).
        return get_posicion(frame_reparametrizado, obj, coord, force_original=True)


    # Coger la lista de fotogramas clave 
    if not obj.animation_data or not obj.animation_data.action:
        
        return obj.location[coord]

    # Buscar f-curve
    fcurve = obj.animation_data.action.fcurves.find('location', index=coord)

    if not fcurve or not fcurve.keyframe_points:
        
        return obj.location[coord]

    keyframes = fcurve.keyframe_points
    keys_list = list(keyframes)

    segment = get_keyframe_segment(keys_list, frm)
    if segment is None:
        return obj.location[coord]

    key0, key1 = segment
    
    if key0 == key1:
        return key0.co[1] # Estamos en un keyframe exacto
    
    #Extraer datos del segmento [t0, t1] y [x0, x1]
    t0, x0 = key0.co
    t1, x1 = key1.co

    method = obj.interpolation_method

    # ----- INTERPOLACIÓN LINEAL -----
    if method == 'LINEAR':
        return interpola.lineal(frm, t0, t1, x0, x1)

    # ----- INTERPOLACIÓN HERMITE -----
    elif method == 'HERMITE':
        # Para Hermite, necesitamos las tangentes (handles)
        m0 = 0.0
        delta_t_h0 = (key0.handle_right[0] - t0)
        if delta_t_h0 != 0:
             m0 = (key0.handle_right[1] - x0) / delta_t_h0
        
        m1 = 0.0
        delta_t_h1 = (key1.handle_left[0] - t1)
        if delta_t_h1 != 0:
            m1 = (key1.handle_left[1] - x1) / delta_t_h1

        return interpola.hermite(frm, t0, t1, x0, x1, m0, m1)

    # ----- INTERPOLACIÓN CATMULL-ROM -----
    elif method == 'CATMULL_ROM':
        idx0 = keys_list.index(key0)
        idx1 = keys_list.index(key1) 

        if idx0 == 0:
            # Para el primer segmento, reflejamos el siguiente punto
            # esto crea una entrada suave al primer keyframe
            t_m1 = t0 - (t1 - t0)
            x_m1 = x0 - (x1 - x0)
        else:
            key_m1 = keys_list[idx0 - 1]
            t_m1, x_m1 = key_m1.co
        
        idx_p2 = idx1 + 1
        if idx_p2 >= len(keys_list):
            # Para el último segmento, reflejamos el punto anterior
            # esto crea una salida suave del último keyframe
            t2 = t1 + (t1 - t0)
            x2 = x1 + (x1 - x0)
        else:
            key2 = keys_list[idx_p2]
            t2, x2 = key2.co

        # Leemos la propiedad de tensión del objeto
        tension = obj.catmull_tension
        return interpola.catmull_rom(frm, t0, t1, x_m1, x0, x1, x2, t_m1, t2, tension)

    # Por defecto
    return interpola.lineal(frm, t0, t1, x0, x1)

    # Identificar entre qué par de fotogramas clave estamos

    # Si está antes del primer fotograma clave
    #if frm <= keyframes[0].co[0]:
        #return keyframes[0].co[1]

    # Si está después del último fotograma clave
     #if frm >= keyframes[-1].co[0]:
         #return keyframes[-1].co[1] 

    # Si está entre dos fotogramas clave
     #key_prev = keyframes[0]
     #for key_next in keyframes:
       #  if key_next.co[0] > frm:
         #    break 
         #key_prev = key_next

    # Interpolación lineal

    # Keyframe anterior
     #frm_prev = key_prev.co[0]
     #val_prev = key_prev.co[1]

    # Keyframe siguiente
     #frm_next = key_next.co[0]
     #val_next = key_next.co[1]

    # Factor de interpolación
     #delta_frm = frm_next - frm_prev
     #if delta_frm == 0:
       #  return val_prev 

     #t = (frm - frm_prev) / delta_frm

    # Fórmula 
     #val_interp = val_prev + t * (val_next - val_prev)

     #return val_interp

### Función para asignar drivers
def asigna_driver_posicion(obj):
    """
        Asigna automáticamente los 3 drivers de posición (X, Y, Z)
        a un objeto dado.
    """

    for i in range(3): # i = 0, 1, 2

        drv = obj.driver_add('location', i).driver

        drv.use_self = True

        drv.expression = f"get_pos(frame, self, {i})"

        print(f"  -> Driver para coordenada {i} creado.")

    if obj.use_orientation_driver:
        
        # Ponemos el modo de rotación a 'QUATERNION' 
        obj.rotation_mode = 'QUATERNION'
        
        # Asignamos los 4 drivers de cuaternión (W, X, Y, Z) 
        for i in range(4): # i = 0 (W), 1 (X), 2 (Y), 3 (Z)
            # El path es 'rotation_quaternion'
            drv = obj.driver_add('rotation_quaternion', i).driver
            drv.use_self = True
            drv.expression = f"get_rot(frame, self, {i})"
            
        print(f"  -> Drivers de Rotación (W,X,Y,Z) creados.")
    
    else:
        # Si el bool es False, borramos los drivers de rotación
        obj.driver_remove('rotation_quaternion')
        print(f"  -> Drivers de Rotación ignorados.")


################### Funciones antiguas #####################

def get_posicion_x_loop(frm: float):
    
    t=frm/24.0
    radio = 5.0
    velocidad_angular = 1.0  

    if t <= 0 :
        posx = 0.0
    else:
        posx = radio * math.cos(velocidad_angular * t)

    return posx

bpy.app.driver_namespace['get_pos_loop_x'] = get_posicion_x_loop

def get_posicion_y_loop(frm: float):
    """
    Devuelve la posición Y de un movimiento circular.
    frm: número de frame actual
    """
    t = frm / 24.0
    radio = 5.0
    velocidad_angular = 1.0
    
    if t <= 0:
        posy = 0.0
    else:
        posy = radio * math.sin(velocidad_angular * t)

    return posy

bpy.app.driver_namespace['get_pos_loop_y'] = get_posicion_y_loop

################### Clases #####################


### Clase del botón
class OBJECT_OT_CreateTrajectory(bpy.types.Operator):
    """Operador que asigna los drivers de trayectoria al objeto activo"""
    bl_idname = "object.create_trajectory_driver"
    bl_label = "Crear Trayectoria Interpolada"
    bl_description = "Asigna drivers a X,Y,Z para interpolar los keyframes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object

        if not obj:
            self.report({'WARNING'}, "No hay objeto activo seleccionado")
            return {'CANCELLED'}

        if not obj.animation_data or not obj.animation_data.action:
            self.report({'WARNING'}, "El objeto no tiene animación (key-frames)")
            return {'CANCELLED'}

        try:
            # 1. PRÁCTICA 4: Pre-calcular la longitud de arco
            # Usamos la función que definimos antes que guarda la curva "distancia_recorrida"
            longitud_total = calcula_longitud_recorrida(obj)
            
            # 2. Inicializar la propiedad 'distancia_deseada' 
            # "insertar dos fotogramas clave... uno en el fotograma 1, con valor 0..."
            
            # Borramos animación previa de esta propiedad para empezar limpio
            # (El try/except evita error si no había keyframes antes)
            try:
                obj.keyframe_delete(data_path="distancia_deseada")
            except RuntimeError:
                pass
            
            # Keyframe en inicio: Distancia 0
            start = int(obj.animation_data.action.frame_range[0])
            obj.distancia_deseada = 0.0
            obj.keyframe_insert(data_path="distancia_deseada", frame=start)
            
            # Keyframe en final: Distancia Total 
            # "...y otro, al final de la animación, con valor la longitud total"
            end = int(obj.animation_data.action.frame_range[1])
            obj.distancia_deseada = longitud_total
            obj.keyframe_insert(data_path="distancia_deseada", frame=end)
            
            # 3. Cambiamos interpolación a LINEAL para velocidad constante 
            # "inicializado la trayectoria de manera que se recorra... a velocidad constante"
            fcurve_dist = obj.animation_data.action.fcurves.find("distancia_deseada")
            if fcurve_dist:
                for kp in fcurve_dist.keyframe_points:
                    kp.interpolation = 'LINEAR'
            
            
            asigna_driver_posicion(obj)
            obj.use_speed_control = True
            
            self.report({'INFO'}, f"Drivers y Control de Velocidad creados. Longitud: {longitud_total:.2f}m")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Fallo al crear drivers: {e}")
            return {'CANCELLED'}
        
class OBJECT_OT_CreateOrientation(bpy.types.Operator):
    """Operador que asigna los drivers de ROTACIÓN al objeto activo"""
    bl_idname = "object.create_orientation_driver"
    bl_label = "Crear Orientación (Rotación)"
    bl_description = "Asigna drivers a la rotación para alinear el objeto con la trayectoria"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if not obj:
            self.report({'WARNING'}, "No hay objeto activo")
            return {'CANCELLED'}
        try:
            asigna_driver_posicion(obj)
            self.report({'INFO'}, f"Drivers de Rotación creados para {obj.name}")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Fallo al crear drivers: {e}")
            return {'CANCELLED'}        


### Clase del panel
### Clase del panel
class VIEW3D_PT_DriversControl(bpy.types.Panel):
    """Crea un Panel en la barra lateral de la Vista 3D"""
    bl_label = "Drivers Control"
    bl_idname = "VIEW3D_PT_drivers_control"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI' 
    bl_category = 'Drivers Control' 

    def draw(self, context):
        layout = self.layout
        obj = context.active_object

        # Caja 1: Trayectoria Básica
        box = layout.box()
        box.label(text="1. Generación Trayectoria")

        if not obj:
            box.label(text="Selecciona un objeto", icon='ERROR')
            return

        if not obj.animation_data or not obj.animation_data.action:
            box.label(text="Añade keyframes al objeto", icon='INFO')

        col = box.column(align=True)
        col.prop(obj, "interpolation_method", text="Algoritmo")
        
        if obj.interpolation_method == 'CATMULL_ROM':
            col.prop(obj, "catmull_tension", text="Tensión")
        
        box.separator()
        box.operator(OBJECT_OT_CreateTrajectory.bl_idname, text="Crear/Actualizar Trayectoria")

        # --- SECCIÓN NUEVA (PRÁCTICA 4) ---
        if obj.animation_data: # Solo mostramos esto si ya hay animación
            box_vel = layout.box()
            box_vel.label(text="2. Control de Velocidad (P4)")
            
            # Checkbox para activar/desactivar la reparametrización
            box_vel.prop(obj, "use_speed_control", text="Activar Control Vel.")
            
            # Si está activo, mostramos la propiedad animable
            if obj.use_speed_control:
                col_vel = box_vel.column(align=True)
                # Mostramos la propiedad 'distancia_deseada'
                # El usuario puede poner el ratón encima y pulsar 'I' para animarla
                col_vel.prop(obj, "distancia_deseada", text="Distancia (m)")
                
                col_vel.label(text="¡Anima 'Distancia' con la tecla I!", icon='KEY_HLT')


        # Caja 3: Rotación
        box_rot = layout.box()
        box_rot.label(text="3. Orientación (Rotación)")
        
        box_rot.prop(obj, "use_orientation_driver")
        
        if obj.use_orientation_driver:
            col_rot = box_rot.column(align=True)
            col_rot.prop(obj, "forward_axis", text="Eje Frontal")
            col_rot.prop(obj, "side_axis", text="Eje Lateral")
            col_rot.prop(obj, "bank_angle", text="Inclinación (Bank)")
            
            box_rot.separator()
            box_rot.operator(OBJECT_OT_CreateOrientation.bl_idname, text="Actualizar Drivers Rotación")

################### Register #####################

### Función registro
def register():
    
    importlib.reload(interpola)

    # Registra las clases 
    for cls in classes:
        bpy.utils.register_class(cls)

    # Registra   la función del driver
    bpy.app.driver_namespace['get_pos'] = get_posicion
    bpy.app.driver_namespace['get_rot'] = get_quaternion_component

    # 1. Propiedad para el método de interpolación
    bpy.types.Object.interpolation_method = bpy.props.EnumProperty(
        items=[
            ('LINEAR', "Lineal", "Interpolación Lineal simple"),
            ('HERMITE', "Hermite", "Interpolación cúbica (usa handles)"),
            ('CATMULL_ROM', "Catmull-Rom", "Spline cúbico (usa tensión)"),
        ],
        name="Método de Interpolación",
        description="Algoritmo a usar para la trayectoria",
        default='LINEAR'
    )
    
    # 2. Propiedad para la tensión de Catmull-Rom
    bpy.types.Object.catmull_tension = bpy.props.FloatProperty(
        name="Tensión",
        description="Tensión para el spline Catmull-Rom (0=estándar)",
        default=0.0,
        min=-1.0, # Permitimos valores negativos
        max=3.0
    )

    bpy.types.Object.forward_axis = bpy.props.EnumProperty(
        items=[
            ('X', "X", "Alinear el eje X con la trayectoria"),
            ('Y', "Y", "Alinear el eje Y con la trayectoria"),
            ('Z', "Z", "Alinear el eje Z con la trayectoria"),
            ('-X', "-X", "Alinear el eje -X con la trayectoria"),
            ('-Y', "-Y", "Alinear el eje -Y con la trayectoria"),
            ('-Z', "-Z", "Alinear el eje -Z con la trayectoria"),
        ],
        name="Eje Frontal",
        description="Eje del objeto que se alineará con la dirección del movimiento",
        default='X'
    )

    bpy.types.Object.side_axis = bpy.props.EnumProperty(
        items=[
            ('X', "X", "Eje lateral (Side) es X"),
            ('Y', "Y", "Eje lateral (Side) es Y"),
            ('Z', "Z", "Eje lateral (Side) es Z"),
            ('-X', "-X", "Eje lateral (Side) es -X"),
            ('-Y', "-Y", "Eje lateral (Side) es -Y"),
            ('-Z', "-Z", "Eje lateral (Side) es -Z"),
        ],
        name="Eje Lateral/Superior",
        description="Eje del objeto que debe mantenerse horizontal (o apuntar hacia arriba)",
        default='Y' # 'Y' suele ser el lateral en coches, 'Z' el superior
    )

    bpy.types.Object.bank_angle = bpy.props.FloatProperty(
        name="Inclinación Lateral (Bank)",
        description="Ángulo de inclinación adicional (alabeo) alrededor de la trayectoria",
        default=0.0,
        unit='ROTATION' # Esto hace que Blender lo muestre en grados
    )

    bpy.types.Object.use_orientation_driver = bpy.props.BoolProperty(
        name="Controlar Rotación",
        description="Activa/desactiva los drivers de rotación",
        default=True
    )
    bpy.types.Object.use_speed_control = bpy.props.BoolProperty(
        name="Usar Control de Velocidad",
        description="Activa la reparametrización por arco",
        default=False
    )
    
    bpy.types.Object.distancia_deseada = bpy.props.FloatProperty(
        name="Distancia Deseada",
        description="Distancia recorrida sobre la curva en metros",
        default=0.0
    )


### Función unregister
def unregister():
    # 1. Desregistrar clases (en orden inverso)
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass

    # 2. Limpiar namespace de drivers
    if 'get_pos' in bpy.app.driver_namespace:
        del bpy.app.driver_namespace['get_pos']
    if 'get_rot' in bpy.app.driver_namespace:
        del bpy.app.driver_namespace['get_rot'] 

    # 3. Eliminar propiedades de Object
    try:
        del bpy.types.Object.interpolation_method
        del bpy.types.Object.catmull_tension
        del bpy.types.Object.forward_axis 
        del bpy.types.Object.side_axis         
        del bpy.types.Object.bank_angle         
        del bpy.types.Object.use_orientation_driver
        del bpy.types.Object.use_speed_control    
        del bpy.types.Object.distancia_deseada    
    except AttributeError:
        pass

def get_quat_from_vecs(e: Vector, t: Vector) -> Quaternion:
    """
    Calcula el cuaternión que alinea el vector 'e' con el vector 't'.
    Usa copias normalizadas como pide el ejercicio.
    """
    e_norm = e.normalized()
    t_norm = t.normalized()
    
    # --- CASOS ESPECIALES ---
    # Si son el mismo vector (paralelos)
    if (e_norm - t_norm).length < 0.0001:
        # No hay rotación, devolver cuaternión identidad
        return Quaternion((1.0, 0.0, 0.0, 0.0))

    # Si son opuestos (anti-paralelos)
    if (e_norm + t_norm).length < 0.0001:
        # Rotación de 180 grados.
        # Necesitamos un eje perpendicular. 
        # 'world_up' o 'world_right' suelen funcionar.
        axis = Vector((0.0, 0.0, 1.0)).cross(e_norm)
        if axis.length < 0.0001: # Si 'e' es (0,0,1)
            axis = Vector((1.0, 0.0, 0.0)).cross(e_norm)

        # Devolvemos un cuaternión de 180º (PI radianes)
        return Quaternion(axis.normalized(), math.pi)


    # 2. Calcular el ángulo 'theta' 
    # El producto escalar nos da el coseno del ángulo
    dot_prod = e_norm.dot(t_norm)
    # Clamp para evitar errores numéricos (ej: 1.0000001)
    dot_prod = max(min(dot_prod, 1.0), -1.0)
    theta = math.acos(dot_prod)
 
    # El producto vectorial nos da un vector perpendicular
    v = e_norm.cross(t_norm)
    v.normalize()

    q = Quaternion(v, theta)

    return q

def get_orientation_quaternion(frame: float, obj) -> Quaternion:
    """
    Función principal que calcula el cuaternión de orientación.
    CORREGIDA: Incluye sincronización con Práctica 4 y arregla variables.
    """
    
    # --- 1. SINCRONIZACIÓN PRÁCTICA 4 (NUEVO) ---
    # Si el control de velocidad está activo, recalculamos el 'frame' real
    # para que la rotación coincida con la posición reparametrizada.
    if getattr(obj, "use_speed_control", False):
        try:
            dist_target = obj.distancia_deseada
        except AttributeError:
            dist_target = frame / 24.0
            
        # Usamos la misma función que usa la posición
        frame = frame_desde_longitud(obj, dist_target)
    # --------------------------------------------

    # Obtener posiciones actual y anterior (Usando force_original=True siempre)
    pos_curr = Vector((
        get_posicion(frame, obj, 0, force_original=True),
        get_posicion(frame, obj, 1, force_original=True),
        get_posicion(frame, obj, 2, force_original=True)
    ))
    # Usamos un delta pequeño para la tangente instantánea
    pos_prev = Vector((
        get_posicion(frame - 0.1, obj, 0, force_original=True),
        get_posicion(frame - 0.1, obj, 1, force_original=True),
        get_posicion(frame - 0.1, obj, 2, force_original=True)
    ))
    
    tangent = pos_curr - pos_prev
    
    if tangent.length < 0.0001:
        return getattr(obj, "rotation_quaternion", Quaternion((1.0, 0.0, 0.0, 0.0)))
    
    tangent.normalize()

    # 1. Obtener el eje frontal del objeto
    e_forward_str = obj.forward_axis
    e_forward_vec = AXIS_VECTORS.get(e_forward_str, Vector((1, 0, 0))) 
    
    # 2. Calcular cuaternión base
    q_align = get_quat_from_vecs(e_forward_vec, tangent)
    
    # 3. CONTROL DE INCLINACIÓN (BANKING)
    
    # Inicializamos q_aligned con el básico por si no entramos en el if de corrección
    q_aligned = q_align 

    e_side_str = obj.side_axis
    e_side_vec = AXIS_VECTORS.get(e_side_str, Vector((0, 1, 0)))
    
    e_side_rotated = q_align @ e_side_vec
    world_up = Vector((0, 0, 1))
    
    if abs(tangent.z) > 0.99:
        reference_up = Vector((0, 1, 0))
    else:
        reference_up = world_up
    
    correction_axis = tangent.cross(reference_up)
    
    if correction_axis.length > 0.001:
        correction_axis.normalize()
        side_projected = e_side_rotated - (e_side_rotated.dot(tangent)) * tangent
        
        if side_projected.length > 0.001:
            side_projected.normalize()
            dot_product = side_projected.dot(reference_up)
            dot_product = max(min(dot_product, 1.0), -1.0)
            correction_angle = math.acos(dot_product)
            
            if correction_axis.dot(side_projected.cross(reference_up)) < 0:
                correction_angle = -correction_angle
            
            q_correction = Quaternion(correction_axis, correction_angle)
            q_aligned = q_correction @ q_align # Aquí actualizamos q_aligned
    
    # 4. Aplicar Bank (Inclinación manual)
    bank_angle_rad = obj.bank_angle
    
    if abs(bank_angle_rad) > 0.0001:
        q_bank = Quaternion(tangent, bank_angle_rad)
        q_final = q_bank @ q_aligned
    else:
        q_final = q_aligned
    
    return q_final

def get_quaternion_component(frame: float, obj, coord: int) -> float:
    """
    Función "wrapper" para el driver .
    Llama a la función principal y devuelve un solo componente (W,X,Y,Z).
    """
    # Llama a la función principal que hace todo el cálculo
    q_final = get_orientation_quaternion(frame, obj)
    
    # Devuelve el componente solicitado (0=W, 1=X, 2=Y, 3=Z)
    return q_final[coord]

### Programa principal

classes = [OBJECT_OT_CreateTrajectory,OBJECT_OT_CreateOrientation,VIEW3D_PT_DriversControl]

if __name__ == "__main__":
    try:
        unregister()
    except:
        pass
    register()
