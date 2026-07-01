# Realizacion de la Practica 1

# I. Descripción y Funcionalidad de la Herramienta

La Práctica 1 ha consistido en el desarrollo de un módulo para Blender, implementado en Python, que permite generar y controlar trayectorias de objetos 3D de forma procedural. El control de la posición se realiza mediante Drivers personalizados que acceden e interpolan los keyframes insertados manualmente por el usuario en el objeto.

### Archivos Implementados
`src/posicion.py` : Contiene la lógica principal: la función `get_posicion()`, la gestión de drivers y la declaración de propiedades de la escena.
`src/interpola.py`: Contiene la implementación de los tres algoritmos de interpolación.

### Funcionalidades Clave

1.  Control por Drivers: La posición del objeto (X, Y, Z) es controlada por la función `get_posicion(frame, self, coord)`, que está registrada como un Driver en Blender. El parámetro `self` permite acceder a los datos del propio objeto, incluyendo sus keyframes.
2.  Interpolación de Keyframes: La herramienta lee los keyframes del objeto (`obj.animation_data.action.fcurves`) y realiza la interpolación entre ellos.
3.  Algoritmos Configurables: Permite al usuario seleccionar entre tres métodos de interpolación mediante una propiedad de la escena:
    * Lineal: Velocidad constante entre keyframes.
    * Hermite: Interpolación basada en velocidades definidas por el usuario.
    * Catmull-Rom: Interpolación suave, con un parámetro de Tensión modificable.
4.  Automatización de Asignación: Un operador automatiza la creación y asignación de los tres drivers de posición (X, Y, Z) al objeto activo.

## II. Forma de Utilización de la Herramienta

La herramienta está integrada en un panel de la interfaz de Blender para un uso intuitivo.

### 1. Preparación del Entorno

1.  Abrir Blender y cargar el script externo que carga `posicion.py` y registra el driver y las propiedades.
2.  Crear o seleccionar un objeto (ej. un cubo o una esfera) en la escena.
3.  Insertar los fotogramas clave de la posición deseada en diferentes puntos del tiempo (utilizando la tecla `I` o `K` en Blender).

### 2. Panel de Control

* Panel:`Drivers Control`
* Propiedades:
    * Algoritmo: Menú desplegable para seleccionar el método de interpolación deseado (Lineal, Hermite, Catmull-Rom).
    * Tensión: Control deslizante visible si se selecciona Catmull-Rom. Permite ajustar la suavidad de la curva.
* Botón:`Crear trayectoria`

### 3. Aplicación de la Trayectoria

1.  Seleccionar el objeto con los keyframes insertados.
2.  En el panel `Drivers Control`, seleccionar el algoritmo deseado (y ajustar la Tensión si se usa Catmull-Rom).
3.  Pulsar el botón `Crear trayectoria`. Esto asigna los drivers a las coordenadas X, Y, Z del objeto.
4.  Lanzar la animación para ver el objeto recorrer la trayectoria interpolada.

## III. Tareas de Validación (Ejercicios 6 y 7)

### Ejercicio 6: Comparación de Algoritmos

Para validar los algoritmos implementados, se creó una escena con tres objetos idénticos. Los tres objetos comparten los mismos fotogramas clave, pero a cada uno se le asignó un método de interpolación distinto (Lineal, Hermite y Catmull-Rom). Esto permite una comparación directa de las propiedades de cada curva:
* Interpolación Lineal genera picos y cambios bruscos de dirección.
* Catmull-Rom genera una trayectoria más suave que pasa por todos los keyframes.
* Hermite muestra el efecto del control adicional sobre las tangentes (velocidades).

### Ejercicio 7: Integración VFX sobre Imagen Real (Circuito)

Este ejercicio será implementado a posteriori en la tarea que se debe entregar el próximo martes 28/10/2025 

