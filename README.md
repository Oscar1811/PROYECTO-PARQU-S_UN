# PROYECTO-PARQUES_UN
El juego de Parqués UN es una versión digital del clásico juego de mesa, desarrollado en Python con Tkinter, donde los jugadores deben mover sus fichas por el tablero hasta llegar a la meta.

Cómo jugar
1. Iniciar el juego
    Ejecuta el archivo main.py para abrir la interfaz del juego.
    Se mostrará el tablero con las posiciones de inicio de cada jugador.
    El primer turno comienza con el jugador de color rojo.
   
2. Lanzar los dados
    Cada turno, el jugador debe presionar el botón "Lanzar Dados".
    Se mostrarán dos valores aleatorios entre 1 y 6.
    Si obtiene un 5, puede sacar una ficha de la cárcel.
    Si obtiene pares, tendrá un turno extra.
    Si saca tres pares seguidos, la última ficha movida regresa a la cárcel.
  
3. Mover las fichas
    Si hay fichas disponibles para mover, se resaltarán en el tablero.
    Haz clic en una ficha resaltada para moverla según el número obtenido en los dados.
    Si una ficha aterriza en una casilla ocupada por otra de un jugador diferente, la ficha capturada regresa a la cárcel.
   
4. Reglas especiales
    Casillas seguras: Algunas posiciones no permiten capturas.
    Camino final: Al llegar a la casilla de entrada al camino final, la ficha debe avanzar con el número exacto hasta la meta.
    Turnos extra: Si capturas una ficha o llegas a la meta, obtienes un movimiento adicional.
   
6. Finalizar turno
    Cuando no haya más movimientos disponibles, el jugador debe presionar "Finalizar Turno" para que el siguiente jugador juegue.

7. Ganar el juego
    El primer jugador que logre llevar todas sus fichas a la meta gana la partida.
    Se mostrará un mensaje anunciando el ganador y se podrá reiniciar el juego.

Juego desarrollado por:
- Oscar David Mogollon Botia
- Juliana Jojoa Rosero
