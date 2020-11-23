'''
Main Driver File
Handles User Input and Current Gamestate Object

'''

import pygame as p
import ChessEngine

p.init()

WIDTH = 512 # Must be divisable by 8
HEIGHT = 512

DIMENSION = 8 # 8x8 Chessboard
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 30
IMAGES = {}

'''
Initialize a global dictionary of images
This will be called exactly once in the main
'''

def loadImages():
	pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
	# Access image with 'IMAGES['wP']'
	for piece in pieces:
		IMAGES[piece] = p.transform.scale(p.image.load('c:/code/Chess/images/' + piece + '.png'), (SQUARE_SIZE, SQUARE_SIZE))

'''
Main Driver
Handles user input and updating  graphics
'''
def main():
	p.init()
	screen = p.display.set_mode((WIDTH, HEIGHT))
	clock = p.time.Clock()
	screen.fill(p.Color('white'))
	gs = ChessEngine.GameState()
	loadImages() # Load Images only once, before while loop

	running = True
	while running: # -------------------- MAIN LOOP -----------------------------------------------
		for e in p.event.get():
			if e.type == p.QUIT:
				running = False
		drawGameState(screen, gs)
		clock.tick(MAX_FPS)
		p.display.flip()


'''
Responsible for all graphics within current game state
'''
def drawGameState(screen, gs):
	drawBoard(screen) # Draw the board
	drawPieces(screen, gs.board) # Draw pieces on top of board
	#TODO: Add Piece Highlighting, Move Suggestions



'''
Draw Board
'''
def drawBoard(screen):
	colors = [p.Color('white'), p.Color('gray')] # The Colors of the Board
	for r in range(DIMENSION):
		for c in range(DIMENSION):
			color = colors[((r+c) % 2)]
			p.draw.rect(screen, color, p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))



'''
Draw Pieces to Board using current GameState.board
'''
def drawPieces(screen, board):
	for r in range(DIMENSION):
		for c in range(DIMENSION):
			piece = board[r][c]
			if piece != '--': # Draw Piece if not on empty square
				screen.blit(IMAGES[piece], p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))




if __name__ == '__main__':
	main()