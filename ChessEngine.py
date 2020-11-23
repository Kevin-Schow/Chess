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


	'''
	Takes a move as parameter and executes it
	Does not work for castling, en-passant, or pawn promotion
	'''
	def makeMove(self, move):
		self.board[move.startRow][move.startCol] = '--'
		self.board[move.endRow][move.endCol] = move.pieceMoved
		self.move_log.append(move) # Log move so can use undo
		self.white_to_move = not self.white_to_move # Swap active player


	'''
	Undo the last move made
	'''
	def undoMove(self):
		if len(self.move_log) != 0: # Make sure there is a move to undo
			move = self.move_log.pop()
			self.board[move.startRow][move.startCol] = move.pieceMoved
			self.board[move.endRow][move.endCol] = move.pieceCaptured
			self.white_to_move = not self.white_to_move # Switch turns back




	'''
	All Moves considering checks
	'''
	def getValidMoves(self):
		return self.getAllPossibleMoves() # TEMPORARY, doesn't look for checks


	'''
	All Moves without considering checks
	'''
	def getAllPossibleMoves(self):
		moves = []
		for r in range(len(self.board))
			for c in range(len(self.board[r])):
				turn = self.board[r][c][0]
				if (turn == 'w' and self.white_to_move) and (turn == 'b' and not self.white_to_move):
					piece = self.board[r][c][1]
					if piece == 'P':
						self.getPawnMoves(r, c, moves)
					elif piece == 'R':
						self.getRookMoves(r, c, moves)
		return moves



	'''
	Get all the Pawn moves at row, column and add these moves to the list
	'''
	getPawnMoves(self, r, c, moves):
		pass



	'''
	Get all the Rook moves at row, column and add these moves to the list
	'''
	getRookMoves(self, r, c, moves):
		pass








class Move():
	# Maps keys to values
	# key: value
	ranksToRows = {'1': 7, '2': 6, '3': 5, '4': 4,
					'5': 3, '6': 2, '7': 1, '8': 0}
	rowToRanks = {v: k for k, v in ranksToRows.items()}
	filesToCols = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
					'e': 4, 'f': 5, 'g': 6, 'h': 7}
	colsToFiles = {v: k for k, v in filesToCols.items()}

	def __init__(self, startSq, endSq, board):
		self.startRow = startSq[0]
		self.startCol = startSq[1]
		self.endRow = endSq[0]
		self.endCol = endSq[1]
		self.pieceMoved = board[self.startRow][self.startCol]
		self.pieceCaptured = board[self.endRow][self.endCol]
		self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol


	'''
	Overriding the equals method
	'''
	def __eq__(self, other):
		if isinstance(other, Move):
			return self.moveID == other.moveID
		return False



	def getChessNotation(self):
		# Gets the Chess Notation of move
		return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)


	def getRankFile(self, r, c):
		return self.colsToFiles[c] + self.rowToRanks[r]

