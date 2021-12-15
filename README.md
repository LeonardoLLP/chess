# Chess

[Dirección del repositorio](https://github.com/LeonardoLLP/chess/)
[Unicode list of pieces](https://unicode-table.com/en/sets/chess-symbols/)

Para este proyecto, hemos realizado diversos pasos por separado, que vamos a intentar resumir lo más posible en pocos párrafos. Lo primero ha sido conseguir imprimir el tablero en la pantalla. Para ello, con memoria del juego del BlackJack, hemos buscado la [lista de carácteres unicode de ajedrez](https://unicode-table.com/en/sets/chess-symbols/) para usarla en la impresión del tablero. Con ella hemos creado dos diccionarios distintos, uno para las piezas negras y otro para las piezas blancas. Hemos también copiado del proyecto del laberinto el método de impresión del laberinto, reajustándolo un poco para que imprima el tablero de ajedrez.

La parte más dificil sin lugar a dudas ha sido la programación de movimientos. Hemos tenido que escribir una lista de movimientos posibles para cada pieza, teniendo en cuenta que algunas varían sus movimiento dependiendo de su posición y de lo que tienen alrededor. Aunque se resuma en dos líneas, este ha sido sin lugar a dudas el mayor quemadero de cabeza.

Por último, hemos tenido que pasar cada pieza en formato unicode a tuples, especificando color y pieza para, ya que el formato unicode no es aceptable en "plain text". El archivo mostrado en "partida.txt" (antes de que se sobreescriba) es uan partida muy corta acabada con un mate pastor.

### Mejoras
Hay que reconocer que el código ha quedado muy incompleto, y tengo que anotar una lista de ideas que no he llegado a implementar por falta de tiempo (en el puente he tenido otros asuntos, y ya me he pasado del plazo con este proyecto) y cómo tenia pensado hacerlo.

En primer lugar, no he programado los enroques. Esto sería lo primero que programaría, ya que tengo muy claro como hacerlo. Implementando cuatro variables (*white_short_castle*, *white_long_castle* y sus análogos para las piezas negras), si se mueve el rey se desactivan ambos y si se mueve una torre se desactiva su respectivo enroque. Y, en el movimiento del rey, se comprueba que si se mueve dos hacia la derecha. su *short_castle* respectivo está disponible, y todas las casillas de en medio (en este caso dos) están libres (== ""), puede hacerlo.

Esto sin embargo da paso a un segundo problema. El rey no puede enrocar ni si está en jaque ni si estaría en jaque en cualquiera de las casilla por las que pasa. Por tanto, habría que programar una función llamada *in_check* que devuelva un bool, y que devuelva **True** si algún movimiento del equipo contrario acabaría en la posición en la que esta. Esta función, hablando sinceramente, no creo que sabría implementarla de manera optima. Podría hacer que el equipo contrario calculara moverse a TODAS las casillas y después vigilase si es válido. Y, justo mientras escribo esto, acabo de darme cuenta de una cosa: solamente hay que calcular la casilla del rey cada vez que se acaba un turno, no hace falta controlar todas las casillas, y re-comprobar si se mueve o si va a enrocar. No es tan dificil ni pesado para el ordenador como yo pensaba.

Por último, la partida se acaba con un ganador cuando el rey es comido, pero normalmente en el ajedrez se acaba con un "jaque-mate". Pero programar esto, teniendo la función de *in_check* programada, es pan comido. Solamente hace falta comprobar, si el rey acaba en jaque después de haber movido, si todas sus jugadas legales también devuelven **True** con la función *in_check*.

Ya como adición, sería muy facil realiar un peqeño programa que lea las partidas hechas, y por tanto, que puedas guardar partidas con distintos nombres y volver a verlas más tarde. Solamente haría falta re-codificarlas, pero eso no supondría un problema: tendríamos que realizar el proceso invertido a lo hecho para codificarlo a "string".

Dejo el código a continuación:

```python
from time import sleep

# Control-flow variables
is_white_turn = True
game_ended = False

white = {
    "king": chr(0x2654),
    "queen": chr(0x2655),
    "rook": chr(0x2656),
    "bishop": chr(0x2657),
    "knight": chr(0x2658),
    "pawn": chr(0x2659)
}
white_pieces = list(white.values())

black = {
    "king": chr(0x265A),
    "queen": chr(0x265B),
    "rook": chr(0x265C),
    "bishop": chr(0x265D),
    "knight": chr(0x265E),
    "pawn": chr(0x265F)
}
black_pieces = list(black.values())

white_list = list(white.values())
black_list = list(black.values())
keys = list(white.keys())  # = list(black.keys())

print(list(white.values()))

# Creating a board
board = []
for i in range(8):
    board.append([])
    for _ in range(8):
        board[i].append("")

print(board)

#! FUNCTIONS - FUNCTIONS - FUNCTIONS - FUNCTIONS - FUNCTIONS - FUNCTIONS

"""Promotes a pawn"""
def promotion(box_: list):
    if is_white_turn:
        colour = white
    else:
        colour = black

    while True:
        promotion_piece = input("Please choose the piece to promote too: ")
        if promotion_piece in keys and promotion_piece not in ["king", "pawn"]:
            board[box_[0]][box_[1]] = colour[promotion_piece]
            break
        else:
            print("Please choose a valid piece (queen, rook, knight or bishop")

"""Checks for end of the game"""
def game_ended():
    board_unpacked = []
    for row in board:
        for place in row:
            board_unpacked.append(place)

    if white["king"] not in board_unpacked or black["king"] not in board_unpacked:
        return True
    else:
        return False


"""Add board to list (of moves)"""
def add_board(board_: list):
    board_.append(board)

"""Add piece to intended spot, easier for the user"""
def add_pieces(places: list, piece: str):
    for place in places:
        board[place[0]-1][place[1]-1] = piece

"""Move piece, independently if it can or not (check done in is_valid function)"""
def move_piece(origin_: list, dest_: list, piece: str):
    board[origin_[0]][origin_[1]] = ""
    board[dest_[0]][dest_[1]] = piece

"""Returns box human-like"""
def get_box(row_, column_):
    try:
        return [int(row_) - 1, int(column_) - 1]
    except:
        return None

"""Obtain piece in intended spot"""
def get_piece(row, column):
    try:
        return board[int(row) - 1][int(column) - 1]
    except:
        return "INVALID PLACE"

"""Determine if a move is valid"""
def is_valid(origin_: list, move_: list, dest_: list, piece_: str, colour_list_: list):
    piece_str = keys[colour_list_.index(piece_)]
    y = move_[0]
    x = move_[1]

    landing = board[dest_[0]][dest_[1]] # To simplify pawn movement function

    if x != 0:
        x_s = int(x / abs(x))
    else:
        x_s = 0  # x sign

    if y != 0:
        y_s = int(y / abs(y))
    else:
        y_s = 0

    cannival = board[dest_[0]][dest_[1]] in colour_list_


    # if landing = piece in my colour list or i don't move, return False
    if move_ == [0, 0]:  # Innecesario: cannival da verdadero ya que es su misma casilla
        return False
    elif cannival:
        return False




    if piece_str == "king":
        if abs(x) <= 1 and abs(y) <= 1:
            return True
        else:
            return False

    elif piece_str == "knight":
        if abs(x) == 1 and abs(y) == 2:
            return True
        elif abs(x) == 2 and abs(y) == 1:
            return True
        else:
            return False

    # Si me preguntas no entiendo ni yo que cojones estoy haciendo.
    # El programa INTENTA iterar por cada posición que tiene que pasar el alfil a ver si está libre. DEBERÍA DE FUNCIONAR.
    # TODO: OPTIMIZAR la repetición de código
    elif piece_str == "bishop":
        if abs(x) == abs(y):
            places_to_pass = [(i * y_s, i * x_s) for i in range(1, abs(x))]
            for place in places_to_pass:
                try:
                    if board[dest_[0]-place[0]][dest_[1]-place[1]] != "":
                        return False
                except:
                    return False
            return True
        else:
            return False


    elif piece_str == "rook":
        if x == 0 or y == 0:
            places_to_pass = [(i * y_s, i * x_s) for i in range(1, max(abs(x), abs(y)))]
            for place in places_to_pass:
                try:
                    if board[dest_[0]-place[0]][dest_[1]-place[1]] != "":
                        return False
                except:
                    return False
            return True
        else:
            return False


    elif piece_str == "queen":
        if x == 0 or y == 0 or abs(x) == abs(y):
            places_to_pass = [(i * y_s, i * x_s) for i in range(1, max(abs(x), abs(y)))]
            for place in places_to_pass:
                try:
                    if board[dest_[0]-place[0]][dest_[1]-place[1]] != "":
                        return False
                except:
                    return False
            return True
        else:
            return False

    #* Sinceramente, no me voy ni a molestar en optimizarlo. Se repite código pero me va a estallar la cabeza.
    elif piece_str == "pawn":
        double_move_enabled = False
        if piece_ == white["pawn"]:
            if origin_[0] == 1:
                double_move_enabled = True
            if abs(x) == y == 1 and landing != "":
                pawn_moves = True
            elif x == 0 and y == 1 and landing == "":
                pawn_moves = True
            elif x == 0 and y == 2 and landing == "" and board[dest_[0]][dest_[1] - 1] == "" and double_move_enabled:
                pawn_moves = True
            else:
                pawn_moves = False

            if pawn_moves and dest_[0] == 7:
                promotion(origin_)
            return pawn_moves


        elif piece_ == black["pawn"]:
            if origin_[0] == 6:
                double_move_enabled = True
            if abs(x) == 1 and y == -1 and landing != "":
                pawn_moves = True
            elif x == 0 and y == -1 and landing == "":
                pawn_moves = True
            elif x == 0 and y == -2 and landing == "" and board[dest_[0]][dest_[1] + 1] == "" and double_move_enabled:
                pawn_moves = True
            else:
                pawn_moves = False

            if pawn_moves and dest_[0] == 0:
                promotion(origin_)
            return pawn_moves



"""Print the board in the "correct" way (white down, black up)"""
def print_board(board_=board):
    for row in range(1, len(board_) + 1):
        # Simplify a bit this variable
        row_to_print = board_[-row]
        print("[", end="")
        for index in range(len(row_to_print)):
            if index != len(row_to_print) - 1:
                print("{:6}".format("\'" + row_to_print[index] + "\', "), end="")
            else:
                print("{:6}".format("\'" + row_to_print[index] + "\'"), end="")
        print("]")

# TODO: Revisar si es optimizable
#! BOARD SETUP
# Add white pieces
add_pieces([(1, 1), (1, 8)], white["rook"])
add_pieces([(1, 2), (1, 7)], white["knight"])
add_pieces([(1, 3), (1, 6)], white["bishop"])
add_pieces([(1, 4)], white["queen"])
add_pieces([(1, 5)], white["king"])

# Add black pieces
add_pieces([(8, 1), (8, 8)], black["rook"])
add_pieces([(8, 2), (8, 7)], black["knight"])
add_pieces([(8, 3), (8, 6)], black["bishop"])
add_pieces([(8, 4)], black["queen"])
add_pieces([(8, 5)], black["king"])

# Add pawns
add_pieces([(2, i) for i in range(1, 9)], white["pawn"])
add_pieces([(7, i) for i in range(1, 9)], black["pawn"])

print_board()


def ask_to_move(colour: dict):
    # Search for white piece in dictonary
    if colour["king"] == white["king"]:
        turn = "white"
        colour_list = white_pieces
    else:
        turn = "black"
        colour_list = black_pieces
    print("It is {} turn".format(turn + "\'s"))

    piece_is_moved = False
    while not piece_is_moved:
        origin_c = input("Please choose a column: ")
        origin_r = input("Please choose a row: ")
        origin_box = get_box(origin_r, origin_c)  # Easier to understand
        origin_piece = get_piece(origin_r, origin_c)


        if origin_piece in list(colour.values()):
            print("Choose where to move your piece")
            dest_c = input("Choose destination column: ")
            dest_r = input("Choose destination row: ")
            dest_box = get_box(dest_r, dest_c)
            dest_piece = get_piece(dest_r, dest_c)
            move_coor = [dest_box[0] - origin_box[0], dest_box[1] - origin_box[1]]


            if dest_piece == "INVALID PLACE":
                print("Destination outside of board")

            elif is_valid(origin_box, move_coor, dest_box, origin_piece, colour_list):
                origin_piece = get_piece(origin_r, origin_c)  # Needed to check for promotion issues
                move_piece(origin_box, dest_box, origin_piece)
                piece_is_moved = True

            else:
                print("Destination isn't valid.")




        elif origin_piece == "INVALID PLACE":
            print("Choose a place inside the board. (Row and column in numbers)")

        elif origin_piece != "":
            print("That is not your piece! You can't move it.")

        else:
            print("You have chosen an empty space. You can't do that.")


# Starting game
game = []
keep_playing = ""
while keep_playing != "0":
    if is_white_turn:
        ask_to_move(white)
    else:
        ask_to_move(black)

    print_board()
    add_board(game)

    if game_ended():
        if is_white_turn:
            print("White won the game!")
        else:
            print("Black won the game!")
        break

    is_white_turn = not is_white_turn
    keep_playing = input("Do you want to keep playing? (0 to exit, enter to continue)")

# Check for move of game
while True:
    review = input("Choose a move to review the board (0 to exit): ")
    try:
        review = int(review)
    except:
        print("That is not a number")
        continue

    try:
        if review == 0:
            break
        else:
            print_board(game[review - 1])
    except:
        print("The number you've chosen is out of range")


#! ENCODE THE GAME TO STRING
for board in game:
    for row in board:
        for piece_i in range(len(row)):
            if row[piece_i] in white_list:
                key = white_list.index(row[piece_i])
                row[piece_i] = (keys[key], "white")
            elif row[piece_i] in black_list:
                key = black_list.index(row[piece_i])
                row[piece_i] = (keys[key], "black")




# Encode the board
# TODO: Need to encode the board to string (tuples)
try:
    f = open("partida.txt", "w")
    for board in game:
        f.write(str(board) + "\n")
finally:
    f.close()
```

