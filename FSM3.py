## Grupo M
## Programadores: Lady Matabanchoy, David Martinez.

## Este codigo, no funcionará aqui dado la libreria GPIO, ya que funciona unicamente en la raspberry.

##Se importan las librerias time,Gpio y los objetos ldr, alarmas.
import math
import RPi.GPIO as GPIO
import time
from ldr import LDRReader
from alarmas2 import Alarma

class RobotControl:
    def __init__(self):
        # Configuración de los pines
        self.IN1 = 36
        self.IN2 = 38
        self.IN3 = 40
        self.IN4 = 37
        self.ENA = 33
        self.ENB = 32
        self.ENCODER1 = 29
        self.ENCODER2 = 31

        # Configuración de GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        GPIO.setup(self.ENCODER1, GPIO.IN)
        GPIO.setup(self.ENCODER2, GPIO.IN)

        # Configuración de PWM
        self.pwmA = GPIO.PWM(self.ENA, 100)
        self.pwmB = GPIO.PWM(self.ENB, 100)

        # Inicia PWM
        self.pwmA.start(0)
        self.pwmB.start(0)

        # Variables para almacenar el estado anterior de los encoders y los contadores de pulsos
        self.pulsos_motor1 = 0
        self.pulsos_motor2 = 0

        # Tiempo de lectura encoders
        self.debounce = 0.001
        self.ultimainterrupcionm1 = time.time()
        self.ultimainterrupcionm2 = time.time()

        # Configurar interrupciones para los encoders
        GPIO.add_event_detect(self.ENCODER1, GPIO.RISING, callback=self.incrementar_pulsos_motor1)
        GPIO.add_event_detect(self.ENCODER2, GPIO.RISING, callback=self.incrementar_pulsos_motor2)

    def incrementar_pulsos_motor1(self, channel):
        if time.time() - self.ultimainterrupcionm1 > self.debounce:
            self.pulsos_motor1 += 1
            self.ultimainterrupcionm1 = time.time()

    def incrementar_pulsos_motor2(self, channel):
        if time.time() - self.ultimainterrupcionm2 > self.debounce:
            self.pulsos_motor2 += 1
            self.ultimainterrupcionm2 = time.time()

    def mover_motor(self, direccion, pulsos_deseados):
        comp = pulsos_deseados
        # Restablecer los contadores de pulsos
        self.pulsos_motor1 = 0
        self.pulsos_motor2 = 0

        # Configurar la dirección del motor
        if direccion == 'atras':
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
            self.pwmA.ChangeDutyCycle(73.5)
            self.pwmB.ChangeDutyCycle(70)
            time.sleep(0.1)
            # Configuración para mover hacia atrás
        elif direccion == 'adelante':
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
            self.pwmA.ChangeDutyCycle(73.5)
            self.pwmB.ChangeDutyCycle(70)
            time.sleep(0.1)
            # Configuración para mover hacia adelante
        elif direccion == 'detener':
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.LOW)
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.LOW)
            self.pwmA.ChangeDutyCycle(0)
            self.pwmB.ChangeDutyCycle(0)
            time.sleep(1)
            # Configuración para detener
        elif direccion == 'giro derecha':
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
            self.pwmA.ChangeDutyCycle(73)
            self.pwmB.ChangeDutyCycle(70)
            time.sleep(0.1)

            # Configuración para girar a la derecha
        elif direccion == 'giro izquierda':
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
            self.pwmA.ChangeDutyCycle(70)
            self.pwmB.ChangeDutyCycle(75)
            time.sleep(0.1)
            # Configuración para girar a la izquierda
        else:
            print("Error, comando no valido.")
            self.pwmA.stop()
            self.pwmB.stop()
            GPIO.cleanup()
            return

        # Mover el motor hasta alcanzar los pulsos deseados
        while self.pulsos_motor1 < comp and self.pulsos_motor2 < comp:
            pass

        # Detener el motor
        self.mover_motor('detener', 0)

def fs3(self,cc): ## Se define la función fs3 que da inicio a la trayectoria
    self.coordenadas = cc
    robot = RobotControl()
    coordenadas = self.coordenadas
    ldr = LDRReader(11)
    alarma = Alarma(18,23,24)

    ## Se establecen los valores y vectores en 0.
    vector_diferencia = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    vector_angulos = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    angulos_grados = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    modulos = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    pulso_angulo_recorrer = 0
    pulso_distancia_recorrer = 0
    origen = [0, 0]
    c = 0
    coordenadas = [origen] + coordenadas

    for i in range(0, 5, 1): ## Se establece hasta un maximo de 5 coordenadas.
        for j in range(0, 2, 1):
            vector_diferencia[i][j] = coordenadas[i + 1][j] - coordenadas[i][j]

    for i in range(0, 5, 1):
        modulos[i] = math.sqrt(vector_diferencia[i][0] ** 2 + vector_diferencia[i][1] ** 2) ## Se calcula el modulo de la diferencia de las coordenadas.
    print("modulos: ", modulos)

    for i in range(0, 5, 1): 
        vector_angulos[i] = math.atan2(vector_diferencia[i][1], vector_diferencia[i][0]) ## Se calcula el angulo de la diferencia de las coordenadas.
    angulos_grados = [math.degrees(angulo) for angulo in vector_angulos] ## Se convierte el angulo de radianes a grados.
    print("angulos: ", angulos_grados)

    while (c != 5 and self.ldr.get_ldr_value()==1): ## Se establece un ciclo cuando las cc son diferentes de 5 y el ldr esta en 1 (bola presente)
        for i in range(0, 5, 1):
            if (vector_angulos[i] >= 0):
                pulso_angulo_recorrer = round(((23 * angulos_grados[i]) / 90)) ## Se calcula el pulso de angulo a recorrer.
                giro = "giro izquierda"
                print(giro, "con: ", pulso_angulo_recorrer, " detener")
                robot.mover_motor(giro, pulso_angulo_recorrer)
                robot.mover_motor("detener", 0)
                pulso_distancia_recorrer = round(((28 * modulos[i] * 10) / 20.3)) ## Se calcula el pulso de distancia a recorrer.
                movimiento = "adelante"

                print(movimiento, "con: ", pulso_distancia_recorrer, " detener")
                robot.mover_motor(movimiento, pulso_distancia_recorrer) ## Se mueve el robot hacia adelante con los pulsos deseados
                robot.mover_motor("detener", 0)
                giro = "giro derecha"
                print(giro, " Se reestablece el angulo")
                robot.mover_motor(giro, pulso_angulo_recorrer) ## Se mueve el robot hacia la derecha con los pulsos deseados
                robot.mover_motor("detener", 0)
                alarma.tocar_buzzer(2) ## Suena el buzzer al llegar a cc intermedia
                c += 1
            else:
                pulso_angulo_recorrer = round(-((20 * angulos_grados[i]) / 90)) ## Se calcula el pulso de angulo a recorrer.
                giro = "giro derecha"
                print(giro, "con: ", pulso_angulo_recorrer, " detener")
                robot.mover_motor(giro, pulso_angulo_recorrer)
                robot.mover_motor("detener", 0)

                pulso_distancia_recorrer = round(((28 * modulos[i] * 10) / 20.3))
                movimiento = "adelante"
                robot.mover_motor(movimiento, pulso_distancia_recorrer)
                robot.mover_motor("detener", 0)
                print(movimiento, "con: ", pulso_distancia_recorrer, " detener")
                giro = "giro izquierda"

                print(giro, " Se reestablece el angulo con :", pulso_angulo_recorrer, "detener") ## Se mueve el robot hacia la izquierda con los pulsos deseados
                robot.mover_motor(giro, pulso_angulo_recorrer)
                robot.mover_motor("detener", 0)
                alarma.tocar_buzzer(2)
                c += 1
    t = 0
    # Calcula el ultimo vector diferencia 
    for j in range (0,2,1):
        vector_diferencia[5][j] = coordenadas[5][j] - coordenadas[0][j]
    # Calcula el modulo del ultimo vector 
    modulos[5] = math.sqrt(vector_diferencia[5][0] ** 2 + vector_diferencia[5][1] ** 2)
    # Calcula el angulo con el eje X del ultimo vector
    vector_angulos[5] = math.atan2(vector_diferencia[5][1], vector_diferencia[5][0])
    angulos_grados[5] = math.degrees(vector_angulos[5])

    while True: ## Ciclo para devolverse, el cual no lograba entrar en la presentación.
        if c==6 and self.ldr.get_ldr_value()==1:
            alarma.encender_led("Verde", 1000)
        elif self.ldr.get_ldr_value()==0:
            if (vector_angulos[5] >= 0):
                pulso_angulo_recorrer = round(((23 * angulos_grados[5]) / 90))
                giro = "giro izquierda"
                print(giro, "con: ", pulso_angulo_recorrer, " detener")
                robot.mover_motor(giro, pulso_angulo_recorrer)
                robot.mover_motor("detener", 0)
                pulso_distancia_recorrer = round(((28 * modulos[5] * 10) / 20.3))
                movimiento = "adelante"

                print(movimiento, "con: ", pulso_distancia_recorrer, " detener")
                robot.mover_motor(movimiento, pulso_distancia_recorrer)
                robot.mover_motor("detener", 0)
                giro = "giro derecha"
                print(giro, " Se reestablece el angulo")
                robot.mover_motor(giro, pulso_angulo_recorrer)
                robot.mover_motor("detener", 0)
                alarma.tocar_encender_led("verde",5)
                t += 1
            else:
                pulso_angulo_recorrer = round(-((20 * angulos_grados[5]) / 90))
                giro = "giro derecha"
                print(giro, "con: ", pulso_angulo_recorrer, " detener")
                robot.mover_motor(giro, pulso_angulo_recorrer)
                robot.mover_motor("detener", 0)

                pulso_distancia_recorrer = round(((28 * modulos[5] * 10) / 20.3))
                movimiento = "adelante"
                robot.mover_motor(movimiento, pulso_distancia_recorrer)
                robot.mover_motor("detener", 0)
                print(movimiento, "con: ", pulso_distancia_recorrer, " detener")
                giro = "giro izquierda"

                print(giro, " Se reestablece el angulo con :", pulso_angulo_recorrer, "detener")
                robot.mover_motor(giro, pulso_angulo_recorrer)
                robot.mover_motor("detener", 0)
                alarma.tocar_buzzer(2)
                t += 1
        break
    return t