
# Servidor C2 con Beacons en Python 
## Introducción 
Este proyecto es una implementación a pequeña escala de un servidor de Comando y Control (C2) utilizando beacons en Python. Fue creado principalmente con el propósito de estudiar programación concurrente y distribuida para un examen en la materia. El proyecto se centra en conceptos fundamentales de ciberseguridad, incluyendo comunicación de red, concurrencia y ejecución de comandos.

## Visión general 
El servidor C2 actúa como un punto de control central para gestionar múltiples agentes, llamados "beacons", desplegados en sistemas objetivo. Estos beacons establecen una conexión persistente con el servidor y esperan comandos. Al recibir un comando del servidor, un beacon ejecuta la acción especificada y reporta los resultados.

## Características
Ejecución de Comandos: El servidor puede enviar comandos a beacons, los cuales son ejecutados en los sistemas objetivo. 

Conexión Persistente: Los beacons mantienen una conexión persistente con el servidor, permitiendo comunicación en tiempo real. 

Concurrencia: Utiliza técnicas de programación concurrente para manejar múltiples conexiones simultáneamente. 

Funcionalidad Básica: El enfoque está en funcionalidades esenciales para entender los principios fundamentales de la comunicación C2. Cómo Funciona 

Inicialización del Servidor: El servidor C2 se inicia, escuchando conexiones entrantes de beacons. 

Despliegue de Beacons: Los beacons son desplegados en sistemas objetivo y configurados para conectarse al servidor. Establecimiento de Conexión: Los beacons establecen una conexión con el servidor al ser desplegados. 

Envío de Comandos: El servidor envía comandos a los beacons conectados. 

Ejecución y Respuesta: Los beacons ejecutan los comandos recibidos y reportan los resultados de vuelta al servidor. Comunicación Continua: El ciclo de comunicación entre el servidor y los beacons asegura un monitoreo y control continuo. 

## Prerrequisitos 
Python 3.x 

Comprensión básica de conceptos de redes 

## Empezar 
1. Clona el repositorio en tu máquina local. 
2. Navega hasta el directorio del proyecto. 
3. Inicia el servidor C2 ejecutando python C2.py. 
4. Cambiar y confugurar direcccion IP y puerto en Beacon a la del C2
5. Despliega el script Beacon.py en sistemas objetivo. 
6. Ejecuta el script del beacon en sistemas objetivo.
7. Interactúa con el servidor C2 enviando comandos a los beacons. 
## Limitaciones 
Limitado a funcionalidades básicas con propósitos educativos. 
Carece de características de seguridad avanzadas encontradas en frameworks C2 profesionales. 
No es adecuado para despliegue en escenarios del mundo real sin mejoras significativas. 
Carece de tecnicas de evasion y cifrado para operaciones Red Team realistas.

Descargo de responsabilidad Este proyecto es solo para fines educativos. El uso no autorizado de este software con fines maliciosos está estrictamente prohibido. Los autores de este proyecto no son responsables de ningún mal uso o daño causado por el software.
