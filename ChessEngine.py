'''
Store All Information About Current State of Chess Game
Determines Valid Moves at Current State
Keeps Move Log

'''
class GameState():
	def __init__(self):
		# Board is 8x8 2d list, each element of list has 2 characters
		# First char = color of piece | 'b' or 'w'
		# Second char = type of piece | 'K', 'Q', 'R', 'B', 'N', 'P'
		# '--' Represents an empty space
		self.board = [
			['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
			['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
			['--', '--', '--', '--', '--', '--', '--', '--'],
			['--', '--', '--', '--', '--', '--', '--', '--'],
			['--', '--', '--', '--', '--', '--', '--', '--'],
			['--', '--', '--', '--', '--', '--', '--', '--'],
			['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
			['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]
		self.white_to_move = True
		self.move_log = []


