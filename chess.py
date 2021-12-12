rows = 8
columns = 8

# Queen unicode: U+2655
white = {
    "king": chr(0x2654),
    "queen": chr(0x2655),
    "rook": chr(0x2656),
    "bishop": chr(0x2657),
    "knight": chr(0x2658),
    "pawn": chr(0x2659)
}

black = {
    "king": chr(0x265A),
    "queen": chr(0x265B),
    "rook": chr(0x265C),
    "bishop": chr(0x265D),
    "knight": chr(0x265E),
    "pawn": chr(0x265F)
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

# TODO: Test
"""Add piece to intended spot, easier for the user"""
def add_pieces(places: list, piece: str):
    for place in places:
        board[place[0]-1][place[1]-1] = piece

add_pieces([(1, 1), (1, 8)], white["rook"])

print(board)

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

