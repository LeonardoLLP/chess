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