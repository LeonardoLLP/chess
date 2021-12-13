rows = 8
columns = 8

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

keys = list(white.keys())  # = list(black.keys())

print(keys)


colours = {
    "white": white,
    "white": black
}

# in case I need it later
checkered_board = chr(0x1F67E)


print(white)
print(black)
print(checkered_board)

# Creating a board
board = []
for i in range(8):
    board.append([])
    for _ in range(8):
        board[i].append("")

print(board)

"""Add piece to intended spot, easier for the user"""
def add_pieces(places: list, piece: str):
    for place in places:
        board[place[0]-1][place[1]-1] = piece

"""Obtain piece in intended spot"""
def get_piece(row: int, column: int):
    try:
        return board[int(row) - 1][int(column) - 1]
    except:
        return "INVALID PLACE"

"""Print the board in the "correct" way (white down, black up)"""
def print_board():
    for row in range(1, len(board) + 1):
        # Simplify a bit this variable
        row_to_print = board[-row]
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
    else:
        turn = "black"
    print("It is {} turn".format(turn + "\'s"))

    origin_r = input("Please choose a row: ")
    origin_c = input("Please choose a column: ")
    origin_box = get_piece(origin_r, origin_c)  # Easier to understand

    if origin_box in list(colour.values()):
        print("Choose where to move your piece")
        dest_r = input("Choose destination row: ")
        dest_c = input("Choose destination column: ")
        dest_box = get_piece(dest_r, dest_c)






    elif origin_box == "INVALID PLACE":
        print("Choose a place inside the board. (Row and column in numbers)")

    elif origin_box != "":
        print("That is not your piece! You can't move it.")

    else:
        print("You have chosen an empty space. You can't do that.")


ask_to_move(white)


print(list(white.values()))

try:
    f = open("partida.txt", "w")
    f.write("Board")
finally:
    f.close()