# Realizacion del Proyecto Final

# I. Descripción del Proyecto

El proyecto final consiste en un video en el que implementamos los conocimientos dados en la asignatura. Este proyecto implementa funcionalidades de los scripts desarrollados en las prácticas, además de vfx con Fspy y composición con luces y props (generación de sombras)

### Archivos Implementados (Scripts del proyecto)
`src/posicion.py` : Contiene la lógica principal: la función `get_posicion()`, la gestión de drivers y la declaración de propiedades de la escena.
`src/interpola.py`: Contiene la implementación de los tres algoritmos de interpolación.

### Funcionalidades Clave del Script

1.  Control por Drivers: La posición del objeto (X, Y, Z) es controlada por la función `get_posicion(frame, self, coord)`, que está registrada como un Driver en Blender. El parámetro `self` permite acceder a los datos del propio objeto, incluyendo sus keyframes.
2.  Interpolación de Keyframes: La herramienta lee los keyframes del objeto (`obj.animation_data.action.fcurves`) y realiza la interpolación entre ellos.
3.  Algoritmos Configurables: Permite al usuario seleccionar entre tres métodos de interpolación mediante una propiedad de la escena:
    * Lineal: Velocidad constante entre keyframes.
    * Hermite: Interpolación basada en velocidades definidas por el usuario.
    * Catmull-Rom: Interpolación suave, con un parámetro de Tensión modificable.
4.  Automatización de Asignación: Un operador automatiza la creación y asignación de los tres drivers de posición (X, Y, Z) al objeto activo.
5. Control de rotación: Alinea los ejes con la tangente para crear la rotación
6. Control de velocidad: Mide las distancias y las guarda para después poder modificarlas a preferencia

## II. Forma de trabajo para el proyecto

Para la elaboración del proyecto se ha partido de la idea de trabajar en escenas separadas repartidas entre los integrantes del grupo. Se ha buscado crear una cierta sintonía y estandarización creando una escena base de la que partan todas (base.blend, en la cual radica el video final), con el el fin de poder obtener los mismos modelados, personajes, animaciones, fspys y luces. Así la tarea de crear cada escena sería semblante a la de montar piezas de puzle, facilitando y agilizando así la elaboración del proyecto.
Base.blend es la rama principal del proyecto, de ahí radican todas sus ramas (escenas), para la comodidad de su uso se ha subdividido la jerarquía, por colecciones: modelados, luces, fspys y personajes(en el que tenemos dos subcolecciones, una de implementacion de cinematica inversa y otra de cinematica directa. Sin subcolección están las capturas de movimiento). La idea de crear el base.blend como anteriormente se ha relatado era con la idea de dividir las escenas equitativamente entre los miembros del grupo, como se podrá comprobar en la redacción de este documento eso no ha sido lo ocurrido, por lo que se pondrá el autor de cada parte del proyecto adjuntado en su apartado, se busca así una evaluación más justa y transparente del proyecto.

### 1. Storyboard

El storyboard se ha realizado en el programa Clip Studio, para la elaboración de este se ha buscado capturar fotogramas clave que orientaran por donde se quería encaminar el proyecto visualmente. Se crearon 16 imágenes.


### 2. Animatic

El animatic se ha realizado en el programa Clip Studio, para la elaboración de este se ha buscado animar fotogramas clave que orientaran por donde se quería encaminar el proyecto visualmente. Se crearon 66 fotogramas aproximadamente, haciendo del animatic de una duración de 23 segundos.


### 3. Guión

El guión fue realizado en Word y su propósito era hacer una idea base de los acontecimientos que se contaban en la historia.


### 4. Material para el proyecto
Los videos realizados se captaron sobre una pista de Scalestric, haciendo planos estáticos y dinámicos. Finalmente los dinámicos no pudieron ser implementados por la complesjidad que suponian cuadrarlos correctamente


Se hicieron capturas de dichos videos para poder postprocesarlos y montar las coordenadas correctamente con Fspy


Los modelados fueron descagados de internet por la complejidad que sumaba al proyecto crearlos desde cero, así que fueron importados.


Los personajes se importaron de las capturas de movimiento realizadas en el aula y la cinematica inversa y directa de las prácticas realizadas con anterioridad.


### 5. Escenas

A continuación se van a detallar de forma específica lo implementado en cada escena


### 5.1 Estadio
Al ser uno de los videos dinámicos grabados se optó por capturar 4 frames que generaran de cierta manera el efecto de profundidad buscado
Se importó como en la mayoría de escenas un estadio y gradas. El estadio al no poder conseguirlo sin un hueco en medio para encajar el circuito se modificó la maya y se eliminaron las caras del medio, creando así el efecto buscado. Se implementaron los personajes como público se posaron pero no se animaron (ya que como se ha dicho antes son 4 frames sueltos). Se creó el plano shadow catcher, la iluminación(en area para simular la fuente de luz de techo con la que se grabaron las escenas). Se configuró el compositing y se exportó en video editing en formato mp4.


### 5.2 Público
Se insertaron gradas y estadio. Lo importante de la escena es la implementación de dos animaciones de captura de movimiento. Una de ellas ha quedado no perfeccionada, aunque se han tocado las fcurves para intentar solventar el error lo máximo  posible.Se creó el plano shadow catcher, la iluminación(en area para simular la fuente de luz de techo con la que se grabaron las escenas). Se configuró el compositing y se exportó en video editing en formato mp4.


### 5.3 Mirada inicial
Se insertaron estadio y los dos vehículos que protagonizan casi en su totalidad la historia. Lo importante de la escena es la implementación de: la animaciones de los conductores por captura de movimiento y la implementación y shading de los coches(son low poly para mejorar las tasas de tiempo de renderizado).Se creó el plano shadow catcher, la iluminación(en area para simular la fuente de luz de techo con la que se grabaron las escenas). Se configuró el compositing y se exportó en video editing en formato mp4.


### 5.4 Arranque carrera
La escena con más errores del proyecto debido a la falta de tiempo para solventarlos, se crearon paths para los vehículos, en esta escena no se usaron los scripts .Se creó el plano shadow catcher, la iluminación(en area para simular la fuente de luz de techo con la que se grabaron las escenas). Se configuró el compositing y se exportó en video editing en formato mp4.


### 5.5 Arranque carrera
La escena con más errores del proyecto debido a la falta de tiempo para solventarlos, se crearon paths para los vehículos, en esta escena no se usaron los scripts .Se creó el plano shadow catcher, la iluminación(en area para simular la fuente de luz de techo con la que se grabaron las escenas). Se configuró el compositing y se exportó en video editing en formato mp4.


### 5.6 Rampa 1 y Rampa 2
La particularidad de estas escenas es que no se pudieron usar los videos capturados del Scalestric y por motivos personales no se pudieron realizar nuevamente. El problema era que la rampa(capturada en el video) estaba muy adentrada en el circuito. Por lo que se optó como solución borrar con el uso de la IA generativa dicha rampa, y en reemplazo se modeló una rampa nueva que si estuviera situada con más naturalidad en la escena. En esta escena si se usó la interpolación con  control de velocidades, la de catmull romm. Hubo otro problema que es notable en el video final, la renderización de la escena se realizó en dos pantallas con saturación muy distinta y esto es apreciable en el resultado final. Para rampa 2 se buscó ajustar las trayectorias para crear en un momento dado un efecto de slow motion. En ambas escenas se creó el plano shadow catcher, la iluminación(en area para simular la fuente de luz de techo con la que se grabaron las escenas. Apoyado de alguna luz puntual para acentuar la perspectiva). Se configuró el compositing y se exportó en video editing en formato mp4.


### 5.7 Acelerador
En esta escena no nos centramos en la imagen/video ya que su intención es mostrarte por dentro del coche como el personaje acelera, para este movimiento se ha hecho uso de cinemática directa. Se creó el plano shadow catcher, la iluminación(luz puntual para poder ver bien los modelados del interior del vehículo). Se configuró el compositing y se exportó en video editing en formato mp4.


### 5.8 Meta
La novedad de esta escena es la implementación de la bandera de meta que va asociada a una captura de movimiento hecha en clase.Están presentes ambos vehículos con su una trayectoria rectilínea. Se creó el plano shadow catcher, la iluminación(en area para simular la fuente de luz de techo con la que se grabaron las escenas.). Se configuró el compositing y se exportó en video editing en formato mp4.


### 5.9 Choque 1 y Choque 2
Se implementó un texto 3D que sirviera de aviso del choque, se usó catmull romm y linear con control de velocidades y se implementó otra captura de movimiento . En ambas escenas se creó el plano shadow catcher, la iluminación(en area para simular la fuente de luz de techo con la que se grabaron las escenas. Apoyado de alguna luz puntual para acentuar la perspectiva). Se configuró el compositing y se exportó en video editing en formato mp4.


### 5.10 Huida coche
Lo más remarcable de la escena a parte del movimiento de los coches es la implementación de una animación del personaje con cinemática inversa, se ajustó lo posible teniendo en cuenta las restricciones, que pueden romper la animación .Se creó el plano shadow catcher, la iluminación(en area para simular la fuente de luz de techo con la que se grabaron las escenas. Apoyado de alguna luz puntual para acentuar la perspectiva). Se configuró el compositing y se exportó en video editing en formato mp4.


### 5.11 Podio
Destaca de esta escena la animación de los dos conductores(captura de movimiento) en la cual se ajustaron las fcurves y se cuadró con el cubo que simula un escalón de podio(aplicación de la práctica del Bob). Se creó el plano shadow catcher, la iluminación(en area para simular la fuente de luz de techo con la que se grabaron las escenas. Apoyado de alguna luz puntual para acentuar la perspectiva). Se configuró el compositing y se exportó en video editing en formato mp4.


### 6. Montaje final del video
Finalmente, se unieron los renders de todas las escenas en el video editing del base.blend y se ajustaron los timings para generar un video fluido de movimiento. Se implementaron efectos de sonido que se obtuvieron de una web de audios sin copyright, buscando así una inmersión en la historia.


### 7. Realización de documentación
Se realiza documentación