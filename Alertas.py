## Grupo M
## Programadores: Lady Matabanchoy, David Martinez.

## Este codigo, no funcionará aqui dado la libreria GPIO, ya que funciona unicamente en la raspberry.

##Se importan las librerias time,Gpio 
import RPi.GPIO as GPIO
import time

class Alarma: ## Se define el objeto Alarmas, que se podria considerar como atributo de la FSM1
    def __init__(self, pin_rojo, pin_verde, buzzer): ## se inicializa las variables y  los pines dados por la FSM1
        self.pin_rojo = pin_rojo
        self.pin_verde = pin_verde
        self.buzzer = buzzer

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin_rojo, GPIO.OUT) ## Se declaran como salidas
        GPIO.setup(self.pin_verde, GPIO.OUT)
        GPIO.setup(self.buzzer, GPIO.OUT)


    def encender_led(self, color, tiempo): ## Función para encender el led depediendo el color, y el tiempo que se le asigne.
        if color == 'rojo':
            GPIO.output(self.pin_rojo, GPIO.HIGH)
            GPIO.output(self.pin_verde, GPIO.LOW)
            time.sleep(tiempo)
            GPIO.output(self.pin_rojo, GPIO.LOW)
        elif color == 'verde':
            GPIO.output(self.pin_rojo, GPIO.LOW)
            GPIO.output(self.pin_verde, GPIO.HIGH)
            time.sleep(tiempo)
            GPIO.output(self.pin_verde, GPIO.LOW)

    def tocar_buzzer(self, tiempo_encendido): ##Función para enceder el buzzer con el tiempo que se le asigne.

        GPIO.output(self.buzzer, GPIO.HIGH)
        time.sleep(tiempo_encendido)

    def alarma_anomalias(self, tiempo_encendido, tiempo_apagado, repeticiones): ##Función usada para anomalias, la cual enciende el buzzer por una cierta cantidad de repeticiones.
        for _ in range(repeticiones):
            GPIO.output(self.buzzer, GPIO.HIGH)
            time.sleep(tiempo_encendido)
            GPIO.output(self.buzzer, GPIO.LOW)
            time.sleep(tiempo_apagado)