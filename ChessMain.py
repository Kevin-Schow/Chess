'''
Main Driver File
Handles User Input and Current gamestate Object

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
	gs = ChessEngine.gameState()
	validMoves = gs.getValidMoves()
	moveMade = False # Flag variable for when a move is made

	loadImages() # Load Images only once, before while loop
	running = True
	square_selected = () # Keep track of last click of user, tuple:(row, col)
	player_clicks = [] # Keep track  of player clicks, two tuples: [(r, c), (r, c)]

	while running: # ---------------------------------------------------------- MAIN LOOP ------------- #
		for e in p.event.get():
			if e.type == p.QUIT:
				running = False
			elif e.type == p.MOUSEBUTTONDOWN: # -------------------------------Mouse Handler ---------- #
				location = p.mouse.get_pos() # (x, y) location of mouse
				col = location[0]//SQUARE_SIZE # These will need to be changed when more panels are added
				row = location[1]//SQUARE_SIZE # Gets mouse pos based on click location on screen
				if square_selected == (row, col): # User clicked same square twice / Deselect
					square_selected = () # Deselect
					player_clicks = [] # Clear Player clicks
				else:
					square_selected = (row, col)
					player_clicks.append(square_selected) # Append first and second clicks
				if len(player_clicks) == 2: # Check if seconds click, if so make move
					move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
					for i in range(len(validMoves)):
						if move == validMoves[i]:
							gs.makeMove(validMoves[i])
							moveMade = True
							square_selected = () # Reset User Clicks
							player_clicks = []
					if not moveMade:
						player_clicks = [square_selected]
			elif e.type == p.KEYDOWN: # -----------------------------------------Key Handler------------ #
				if e.key == p.K_z: # Undo -- 'z'
					gs.undoMove()
					moveMade = True
		if moveMade:
			animateMove(gs.moveLog[-1], screen, gs.board, clock)
			validMoves = gs.getValidMoves() # Generate valid move after a move is made
			moveMade = False
		drawGameState(screen, gs, validMoves, square_selected)
		clock.tick(MAX_FPS)
		p.display.flip()


'''
Highlight Square Selected and moves for piece selected
'''
def highlightSquares(screen, gs, validMoves, square_selected):
	if square_selected != ():
		r, c = square_selected
		if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): # Make sure a piece that can be moved is selected
			# Highlight selected square
			s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
			s.set_alpha(100) # Transparency Value 0-255
			s.fill(p.Color('blue'))
			screen.blit(s, (c*SQUARE_SIZE, r*SQUARE_SIZE))
			# Highlight moves from square
			s.fill(p.Color('yellow'))
			for move in validMoves:
				if move.startRow == r and move.startCol == c:
					screen.blit(s, (move.endCol*SQUARE_SIZE, move.endRow*SQUARE_SIZE))



'''
Responsible for all graphics within current game state
'''
def drawGameState(screen, gs, validMoves, square_selected):
	drawBoard(screen) # Draw the board
	highlightSquares(screen, gs, validMoves, square_selected)
	drawPieces(screen, gs.board) # Draw pieces on top of board
	



'''
Draw Board
'''
def drawBoard(screen):
	global colors
	colors = [p.Color('white'), p.Color('gray')] # The Colors of the Board
	for r in range(DIMENSION):
		for c in range(DIMENSION):
			color = colors[((r+c) % 2)]
			p.draw.rect(screen, color, p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))



'''
Draw Pieces to Board using current gameState.board
'''
def drawPieces(screen, board):
	for r in range(DIMENSION):
		for c in range(DIMENSION):
			piece = board[r][c]
			if piece != '--': # Draw Piece if not on empty square
				screen.blit(IMAGES[piece], p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


'''
Animating a Move
'''
def  animateMove(move, screen, board, clock):
	global colors
	dR = move.endRow - move.startRow
	dC = move.endCol - move.startCol
	framesPerSquare = 10 # Frames to move one square
	frameCount = (abs(dR) + abs(dC)) * framesPerSquare
	for frame in range(frameCount + 1):
		r, c =(move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
		drawBoard(screen)
		drawPieces(screen, board)
		# Erase piece moved from ending square
		color = colors[(move.endRow + move.endCol) % 2]
		endSquare = p.Rect(move.endCol*SQUARE_SIZE, move.endRow*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
		p.draw.rect(screen, color, endSquare)
		# Draw captured piece onto rectangle
		if move.pieceCaptured != '--':
			screen.blit(IMAGES[move.pieceCaptured], endSquare)
		# Draw moving piece
		screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
		p.display.flip()
		clock.tick(60)




if __name__ == '__main__':
	main()