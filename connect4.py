import numpy as np
import pygame
import sys
import math

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

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


# For testing
# def print_board(board):
# 	print(np.flip(board, 0))

def draw_board(board):
	board = np.flip(board, 0)
	for c in range(COL_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			if board[r][c] == 0:
				pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 1:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
			else:
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()


board = create_board()
game_over = False
turn = 0

# print_board(board)
pygame.init()

SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)

width = COL_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()


myfont = pygame.font.SysFont("Georgia", 75)

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == 0:
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
			else:
				pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
			pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
			posx = event.pos[0] # x position of mouse
			col = int(math.floor(posx / SQUARESIZE))
	 
			player = int(turn)+1

			if is_valid_location(board, col):
				row = get_next_open_row(board, col)
				board = drop_piece(board, row, col, player)

			if gameWon(board, col):
				game_over = True
				message = "Player {0} wins!".format(player)
				label = myfont.render(message, 1, WHITE)
				screen.blit(label, (10,10))
				# print("Player %d wins!" % player)


			# print_board(board)
			draw_board(board)

			turn += 1
			turn = turn % 2

			if game_over:
				pygame.time.wait(3000)
