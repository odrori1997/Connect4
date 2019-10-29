import numpy as np

ROW_COUNT = 6
COL_COUNT = 7

def create_board():
	board = np.zeros((ROW_COUNT, COL_COUNT))
	return board

def drop_piece(board, row, col, player):
	if is_valid(board, row, col):
		board[row][col] = player
	return board

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0 and is_valid(board, col, 0)

def is_valid(board, col, row):
	return row >= 0 and row < len(board) and col >= 0 and col < len(board[0])

def get_next_open_row(board, col):
	for i in range(ROW_COUNT):
		if board[i][col] == 0:
			return i
	return -1

def gameWon(board, col):
	row = get_next_open_row(board, col) - 1
	dirs = [(0,1), (1,1), (-1,1), (1,0)]
	for dir in dirs:
		across = 0
		newRow = row
		newCol = col
		while is_valid(board, newCol, newRow) and board[newRow][newCol] == board[row][col]:
			newRow += dir[0]
			newCol += dir[1]
			across += 1
		newRow = row
		newCol = col
		while is_valid(board, newCol, newRow) and board[newRow][newCol] == board[row][col]:
			newRow -= dir[0]
			newCol -= dir[1]
			across += 1

		if across-1 >= 4:
			return True

	return False

def print_board(board):
	print(np.flip(board, 0))


board = create_board()
print_board(board)
game_over = False
turn = 0

while not game_over:
	if turn == 0:
		col = int(input("Player 1 enter a column (0-6):"))

	else:
		col = int(input("Player 2 enter a column (0-6):"))

	if is_valid_location(board, col):
		row = get_next_open_row(board, col)
		board = drop_piece(board, row, col, turn+1)

	if gameWon(board, col):
		game_over = True
		print("Player %d won!" % turn+1)

	print_board(board)


	turn += 1
	turn = turn % 2
