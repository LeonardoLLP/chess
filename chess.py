# rows = 8
# columns = 8

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




"""Move piece, independently if it can or not (check done in is_valid function)"""
def move_piece(origin_: list, dest_: list, piece: str):
    board[origin_[0]][origin_[1]] = ""
    board[dest_[0]][dest_[1]] = piece

def get_box(row_, column_):
    return [int(row_) - 1, int(column_) - 1]

"""Obtain piece in intended spot"""
def get_piece(row, column):
    try:
        return board[int(row) - 1][int(column) - 1]
    except:
        return "INVALID PLACE"

"""Determine if a move is valid"""
def is_valid(move_: list, dest_: list, piece_: str, colour_list_: list):
    piece_str = keys[colour_list_.index(piece_)]
    x = move_[1]
    y = move_[0]

    cannival = get_piece(dest_[0], dest_[1]) in colour_list_

    if move_ == [0, 0]:
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



    elif piece_str == "bishop":
        pass

    elif piece_str == "rook":
        pass

    elif piece_str == "queen":
        pass

    elif piece_str == "pawn":
        pass




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
        colour_list = white_pieces
    else:
        turn = "black"
        colour_list = black_pieces
    print("It is {} turn".format(turn + "\'s"))

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
        elif is_valid(move_coor, dest_box, origin_piece, colour_list):
            move_piece(origin_box, dest_box, origin_piece)
        else:
            print("Destination isn't valid.")




    elif origin_piece == "INVALID PLACE":
        print("Choose a place inside the board. (Row and column in numbers)")

    elif origin_piece != "":
        print("That is not your piece! You can't move it.")

    else:
        print("You have chosen an empty space. You can't do that.")


ask_to_move(white)



try:
    f = open("partida.txt", "w")
    f.write("Board")
finally:
    f.close()