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
		self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
		
		self.white_to_move = True
		self.move_log = []
		self.whiteKingLocation = (7, 4)
		self.blackKingLocation = (0, 4)
		# self.inCheck = False
		# self.pins = []
		# self.checks = []



		self.checkMate = False
		self.staleMate = False



	'''
	Takes a move as parameter and executes it
	Does not work for castling, en-passant, or pawn promotion
	'''
	def makeMove(self, move):
		self.board[move.startRow][move.startCol] = '--'
		self.board[move.endRow][move.endCol] = move.pieceMoved
		self.move_log.append(move) # Log move so can use undo
		self.white_to_move = not self.white_to_move # Swap active player
		# Update King's location if moved
		if move.pieceMoved == 'wK':
			self.whiteKingLocation = (move.endRow, move.endCol)
		elif move.pieceMoved == 'bK':
			self.blackKingLocation = (move.endRow, move.endCol)


	'''
	Undo the last move made
	'''
	def undoMove(self):
		if len(self.move_log) != 0: # Make sure there is a move to undo
			move = self.move_log.pop()
			self.board[move.startRow][move.startCol] = move.pieceMoved
			self.board[move.endRow][move.endCol] = move.pieceCaptured
			self.white_to_move = not self.white_to_move # Switch turns back
			# Update King's location if moved
			if move.pieceMoved == 'wK':
				self.whiteKingLocation = (move.startRow, move.startCol)
			elif move.pieceMoved == 'bK':
				self.blackKingLocation = (move.startRow, move.startCol)



	'''
	All Moves considering checks
	'''
	def getValidMoves(self):
		# Generate all possible moves
		moves = self.getAllPossibleMoves()
		# For each move, make the move
		for i in range(len(moves)-1, -1, -1): # Iterate backwards to avoid bug
			self.makeMove(moves[i])
			# Generate all opponent moves
			# For each opponent move, see if they attack your king
			self.white_to_move = not self.white_to_move
			if self.inCheck():
				moves.remove(moves[i]) # If they do, not a valid move
			self.white_to_move = not self.white_to_move
			self.undoMove()
		if len(moves) == 0: # Checkmate or Stalemate
			if self.inCheck():
				self.checkMate = True
			else: self.staleMate = True
		else:
			self.checkMate = False
			self.staleMate = False		
		return moves

	'''
	Determine if current player in check
	'''
	def inCheck(self):
		if self.white_to_move:
			return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
		else:
			return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])



	'''
	Determine if the enemy can attack square (r, c)
	'''
	def squareUnderAttack(self, r, c):
		self.white_to_move = not self.white_to_move # Switch to opponent turn
		oppMoves = self.getAllPossibleMoves()
		self.white_to_move = not self.white_to_move # Switch turns back
		for move in oppMoves:
			if move.endRow == r and move.endCol == c: # Square under attack
				return True
		return False




	'''
	All Moves without considering checks
	'''
	def getAllPossibleMoves(self):
		moves = []
		for r in range(len(self.board)):
			for c in range(len(self.board[r])):
				turn = self.board[r][c][0]
				if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
					piece = self.board[r][c][1]
					self.moveFunctions[piece](r, c, moves) # Call appropriate move function for each piece type
		return moves



	'''
	Get all the Pawn moves at row, column and add these moves to the list
	'''
	def getPawnMoves(self, r, c, moves):
		if self.white_to_move: # White Pawn moves
			if self.board[r-1][c] == '--': # 1 square pawn advance
				moves.append(Move((r , c), (r-1, c), self.board))
				if r == 6 and self.board[r-2][c] == '--': # 2 square pawn advance
					moves.append(Move((r , c), (r-2, c), self.board))
			if c-1 >= 0: # Capture to the left
				if self.board[r-1][c-1][0] == 'b': # Enemy piece to capture
					moves.append(Move((r , c), (r-1, c-1), self.board))
			if c+1 <= 7: # Capture to the right
				if self.board[r-1][c+1][0] == 'b': # Enemy piece to capture
					moves.append(Move((r , c), (r-1, c+1), self.board))

		else:
			# Black Pawn moves
			if self.board[r+1][c] == '--': # 1 square pawn advance
				moves.append(Move((r , c), (r+1, c), self.board))
				if r == 1 and self.board[r+2][c] == '--': # 2 square pawn advance
					moves.append(Move((r , c), (r+2, c), self.board))
			if c-1 >= 0: # Capture to the left
				if self.board[r+1][c-1][0] == 'w': # Enemy piece to capture
					moves.append(Move((r , c), (r+1, c-1), self.board))
			if c+1 <= 7: # Capture to the right
				if self.board[r+1][c+1][0] == 'w': # Enemy piece to capture
					moves.append(Move((r , c), (r+1, c+1), self.board))
			
			




	'''
	Get all the Rook moves at row, column and add these moves to the list
	'''
	def getRookMoves(self, r, c, moves):
		directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
		enemyColor = 'b' if self.white_to_move else 'w'
		for d in directions:
			for i in range(1, 8):
				endRow = r + d[0] * i
				endCol = c + d[1] * i
				if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
					endPiece = self.board[endRow][endCol]
					if endPiece == '--': # Empty space valid
						moves.append(Move((r, c), (endRow, endCol), self.board))
					elif endPiece[0] == enemyColor: # Enemy piece valid
						moves.append(Move((r, c), (endRow, endCol), self.board))
						break
					else: # Friendly piece invalid
						break
				else: # Off board
					break



	'''
	Get all the Knight moves at row, column and add these moves to the list
	'''
	def getKnightMoves(self, r, c, moves):
		knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
		allyColor = 'w' if self.white_to_move else 'b'
		for m in knightMoves:
			endRow = r + m[0]
			endCol = c + m[1]
			if 0 <= endRow < 8 and 0 <= endCol < 8:
				endPiece = self.board[endRow][endCol]
				if endPiece[0] != allyColor: # Not an ally piece (empty or enemy color)
					moves.append(Move((r, c), (endRow, endCol), self.board))
			
				


	'''
	Get all the Bishop moves at row, column and add these moves to the list
	'''
	def getBishopMoves(self, r, c, moves):
		directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
		enemyColor = 'b' if self.white_to_move else 'w'
		for d in directions:
			for i in range(1, 8):
				endRow = r + d[0] * i
				endCol = c + d[1] * i
				if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
					endPiece = self.board[endRow][endCol]
					if endPiece == '--': # Empty space valid
						moves.append(Move((r, c), (endRow, endCol), self.board))
					elif endPiece[0] == enemyColor: # Enemy piece valid
						moves.append(Move((r, c), (endRow, endCol), self.board))
						break
					else: # Friendly piece invalid
						break
				else: # Off board
					break



		'''
	Get all the Queen moves at row, column and add these moves to the list
	'''
	def getQueenMoves(self, r, c, moves):
		self.getRookMoves(r, c, moves)
		self.getBishopMoves(r, c, moves)



		'''
	Get all the King moves at row, column and add these moves to the list
	'''
	def getKingMoves(self, r, c, moves):
		kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
		allyColor = 'w' if self.white_to_move else 'b'
		for i in range(8):
			endRow = r + kingMoves[i][0]
			endCol = c + kingMoves[i][0]
			if 0 <= endRow < 8 and 0 <= endCol < 8:
				endPiece = self.board[endRow][endCol]
				if endPiece[0] != allyColor: # Not an ally (empty or enemy piece)
					moves.append(Move((r, c), (endRow, endCol), self.board))








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

