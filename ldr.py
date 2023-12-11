## Grupo M
## Programadores: Lady Matabanchoy, David Martinez.

## Este codigo, no funcionará aqui dado la libreria GPIO, ya que funciona unicamente en la raspberry.

##Se importan las librerias time,Gpio
import RPi.GPIO as GPIO
import time

class LDRReader: ## Se crea un objeto de la clase LDRReader
    def __init__(self, ldr_pin):
        self.ldr_pin = ldr_pin
        self.ldr_value = None
        GPIO.setmode(GPIO.BOARD) 
        GPIO.setwarnings(False)
        GPIO.setup(self.ldr_pin, GPIO.IN)

    def read_ldr(self): ##Se define la lectura del sensor ldr
        try:
            self.ldr_value = 1 if GPIO.input(self.ldr_pin) else 0 ## Se definen los valores como 1 y 0, para que en el manejo de las fsm's sea mas sencillo
            print("Valor LDR:", self.ldr_value)
            time.sleep(1)
            GPIO.cleanup()
        except KeyboardInterrupt:
            GPIO.cleanup()

    def get_ldr_value(self):  ##Se toma el valor devuelto por el sensor y este es el que se usa para continuar con los ciclos en los diferentes codigos.
        if self.ldr_value is None:
            self.read_ldr()
        return self.ldr_value
