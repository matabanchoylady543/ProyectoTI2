## Grupo M
## Programadores: Lady Matabanchoy, David Martinez.

## Este codigo, no funcionará aqui dado la libreria GPIO, ya que funciona unicamente en la raspberry.

##Se importan las librerias time,Gpio y los objetos de recepción trayectoria, ldr, alarmas, control de motores.
import time
import RPi.GPIO as GPIO
from recepcion_trayectoria import RecepTrayectoria
from ldr import LDRReader
from alarmas import Alarma
from mover_motores import RObotMov




## Creación de variables inicializadas en 0, además de los objetos.
activacionFSm1 = 0
estados = 0
t=0
ldr=LDRReader(11)
alarma = Alarma(18,23,24)
recepcion = RecepTrayectoria()
coordenadas = []
coordenadas_cambiadas = []
motores = RobotMov

while (activacionFSm1 != 1): #Boton de activación FSM1
  print('Estado S0 maquina principal')
  activacionFSm1= int(input("Activación robot: "))
  estados =+ 1
while (activacionFSm1==1 and estados !=4 ):
  if estados == 1:
    coordenadas, coordenadas_cambiadas, t = recepcion.recepcion_trayectoria() ## Se llama a la FSM2- Recepción de trayectoria, además de pedir coordenadas.
    estados = estados + 1
  elif estados == 2:
    print('Estado S2 - FSM-1')
    c = 0
    Temporizador = 5 #Tiempo de espera para que se ponga la bola
    while c != 1:

      if ldr.get_ldr_value()==1: 
        print('Presencia de la bola detectada')

        estados = estados + 1
        c = 1
        print("==========================================")
      else:
        for i in range(5,0,-1):
          print(i)
          time.sleep(1)
          Temporizador = Temporizador - 1
        if Temporizador == 0:

            alarma.encender_led("verde",2) 
            
            Temporizador = 5
            print("==========================================")
  elif estados==3:
    print('Estado S3 - FSM-1')
    motores.fs3(coordenadas) ## Se llama a la FSM3- Movimiento de robot.
    print('Trayectoria completada exitosamente')
    print("==========================================")
    break
GPIO.cleanup()
