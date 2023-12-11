## Grupo M
## Programadores: Lady Matabanchoy, David Martinez.

## Este codigo, no funcionará aqui dado la libreria GPIO, ya que funciona unicamente en la raspberry.


class RecepTrayectoria: ## Se maneja como un objeto la FSM3
  def __init__(self): #Se inicializan los valores propios del objeto.
      self.v = []
      self.w = []
      self.r = []
      self.s = []
      self.coordenadas = []
      self.coordenadas_cambiadas = []
      self.estados = 0
      self.t = 0

  def ingresar_coordenadas(self):
    #Funcion que ingresa las coordenadas de las trayectorias en el tablero
    matriz_coordenadas = [] 
    #Se declara la matriz de coordenadas
    while True:
      try:
        for i in range(5):
          while True:
            try:
              x = float(input(f"Ingrese la coordenada x{i + 1}: "))
              y = float(input(f"Ingrese la coordenada y{i + 1}: "))
              #Se ingresan las coordenadas
              if -20 <= x <= 20 and -20 <= y <= 20:
                coordenada = [x, y]
                matriz_coordenadas.append(coordenada)
                #Se agrega la coordenada condicionada a la matriz
                break
              else:
                print("Las coordenadas deben estar en el rango de -20 a 20. Intente nuevamente.")

            except ValueError:
              print("¡Error! Debe ingresar un número válido.")

        return matriz_coordenadas
      except ValueError:
        print("¡Error! Debe ingresar un número válido para el número de coordenadas.")

  def pedir_vector(self, nombre): #Se piden los vectores para las posiciones.
    while True:
      try:
        n = float(input(f"Ingresa la posición x para {nombre}: "))
        m = float(input(f"Ingresa la posición y para {nombre}: "))
        if -20 <= n <= 20 and -20 <= m <= 20:
          x = n
          y = m
          break
        else:
          print("Las coordenadas deben estar en el rango de -20 a 20. Intente nuevamente.")
      except ValueError:
        print("¡Error! Debe ingresar un número válido.")
    return [x, y]      

  def calcular_determinante(self, matriz): #Cálculo del determinante de la matriz N
    return ((matriz[0][0] * matriz[1][1]) - (matriz[0][1] * matriz[1][0]))

  def calcular_adjunta(self, matriz): #Cálculo de la matriz adjunta
    return [[matriz[1][1], -matriz[0][1]], [-matriz[1][0], matriz[0][0]]]

  def multiplicar_matriz(self, a, b): 
    if len(a[0]) != len(b):
      print("dimensiones incompatibles.")
      exit()
    result = [[sum(a[i][k] * b[k][j] for k in range(len(a[0])))
        for j in range(len(b[0]))] for i in range(len(a))]
    result = [[round(elemento, 2) for elemento in fila] for fila in result]
    #para redondear el resultado
    return result

  def recepcion_trayectoria(self):
    t=0 # Salida para verificar si ya se completo o no la Fsm-Trayectoria
    #Ingresa valores de la base B 
    a = 1
    self.estados=1
    while(a==1 and self.estados != 4):
      if self.estados==1:
        print('Estado s1 de FSM-1 = Estado S0 FSM-2')
        print('Estado S1')
        print("Ingrese los valores para los vectores v,w de la base B:")
        self.v = self.pedir_vector('v')
        self.w = self.pedir_vector('w')
        #Ingresa valores base N
        print("Ingrese los valores para los vectores r,s de la base N")
        self.r = self.pedir_vector('r')
        self.s = self.pedir_vector('s')
        print("==========================================")
        self.estados = self.estados +1
      elif self.estados ==2:
        print('Estado S2')
        self.coordenadas = self.ingresar_coordenadas()
        self.estados = self.estados +1
      elif self.estados == 3:
        print('Estado S3')
        matriz_n = [self.r[0], self.s[0]], [self.r[1], self.s[1]] #Orden en columnas
        print("Matriz N:", matriz_n)
        matriz_bc =[self.v[0], self.w[0]], [self.v[1], self.w[1]] #Matriz B-C
        print("Matriz b:", matriz_bc)
        matriz_adj = self.calcular_adjunta(matriz_n) #Ahora se hace matriz adjunta
        print("Adjunta:", matriz_adj)
        determinante = self.calcular_determinante(matriz_n)#Calculo del determinante
        if determinante == 0: ## Condición del determinante
          print("¡Error!, la matriz no tiene inversa, el determinante es:",
              determinante)
          self.recepcion_trayectoria() ## Se le pide nuevamente al usuario los valores
        else: 
          print("Determinante:", determinante) ## Si el determinante es diferente de 0, continua.

        matriz_inv = [[elemento * 1 / determinante for elemento in fila] for fila in matriz_adj] 
        #Matriz Inversa
        print("La matriz inversa: ", matriz_inv)
        #Multiplicacion de matriz_bc*matriz_inv y declaracion de matriz_ban
        matriz_ban = self.multiplicar_matriz(matriz_inv, matriz_bc)
        print("La matriz de cambio base", matriz_ban)
        print("==========================================")
      #Se inicia la recepcion de datos de trayectoria
        'coordenadas = ingresar_coordenadas()'
        'print("==========================================")'
      #Impresion de coordenadas intermedias
        for i in range(len(self.coordenadas) - 1):
          print(f"Ubicacion Intermedia Original {i + 1}:({self.coordenadas[i][0]}, {self.coordenadas[i][1]})")

      #Impresion de coordenadas finales
        print(f"Ubicacion Final Original:({self.coordenadas[-1][0]}, {self.coordenadas[-1][1]})")
        print("==========================================")

      #Multiplicacion de matriz_ban*coordenadas
        for x, y in self.coordenadas:
          x_cambiado = matriz_ban[0][0] * x + matriz_ban[0][1] * y
          y_cambiado = matriz_ban[1][0] * x + matriz_ban[1][1] * y
          self.coordenadas_cambiadas.append([x_cambiado, y_cambiado])
      #Impresion de coordenadas cambiadas de base
        print("Coordenadas Base Base N:")
        for i in range(len(self.coordenadas_cambiadas) - 1):
          print(f"Ubicacion Intermedia Base N {i + 1}:({round(self.coordenadas_cambiadas[i][0], 3)}, {round(self.coordenadas_cambiadas[i][1], 3)})")

        print(f"Ubicacion Final Base N:({round(self.coordenadas_cambiadas[-1][0], 3)}, {round(self.coordenadas_cambiadas[-1][1], 3)})")
        print("==========================================")
        t = t + 1
        break
    return self.coordenadas, self.coordenadas_cambiadas, t ## Devuelve las coordenadas canonicas, las coordenadas en matriz de cambio y la salida de la FSM-Trayectoria

