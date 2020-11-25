'''
Store All Information About Current State of Chess Game
Determines Valid Moves at Current State
Keeps Move Log

'''
class gameState():
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
		
		self.whiteToMove = True
		self.move_log = []
		self.whiteKingLocation = (7, 4)
		self.blackKingLocation = (0, 4)
		self.inCheck = False
		self.pins = []
		self.checks = []

		self.checkMate = False
		self.staleMate = False
		self.isEnpassantMove = () # Coordinates for square where enpassant possible

	'''
	Takes a move as parameter and executes it
	Does not work for castling, en-passant, or pawn promotion
	'''
	def makeMove(self, move):
		self.board[move.startRow][move.startCol] = '--'
		self.board[move.endRow][move.endCol] = move.pieceMoved
		self.move_log.append(move) # Log move so can use undo
		self.whiteToMove = not self.whiteToMove # Swap active player
		# Update King's location if moved
		if move.pieceMoved == 'wK':
			self.whiteKingLocation = (move.endRow, move.endCol)
		elif move.pieceMoved == 'bK':
			self.blackKingLocation = (move.endRow, move.endCol)
		# Pawn Promotion
		if move.isPawnPromotion:
			self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'
		# En Passant
		if move.isEnpassantMove:
			self.board[move.startRow][move.endRow] = '--' # Capture the pawn
		# Update empassntPossible var
		if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2: # 2 square pawn advance
			self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
		else:
			self.enpassantPossible = ()


	'''
	Undo the last move made
	'''
	def undoMove(self):
		if len(self.move_log) != 0: # Make sure there is a move to undo
			move = self.move_log.pop()
			self.board[move.startRow][move.startCol] = move.pieceMoved
			self.board[move.endRow][move.endCol] = move.pieceCaptured
			self.whiteToMove = not self.whiteToMove # Switch turns back
			# Update King's location if moved
			if move.pieceMoved == 'wK':
				self.whiteKingLocation = (move.startRow, move.startCol)
			elif move.pieceMoved == 'bK':
				self.blackKingLocation = (move.startRow, move.startCol)
			# Undo Enpassant
			if move.isEnpassantMove:
				self.board[move.endRow][move.endCol] = '--' # Leave landing square blank
				self.board[move.startRow][move.endCol] = move.pieceCaptured
				self.enpassantPossible = (move.endRow, move.endCol)
			# Undo 2 square pawn advance
			if move.pieceMoved == 'P' and abs(move.startRow - move.endRow) == 2:
				self.enpassantPossible = ()


	'''
	All Moves considering checks
	'''

	# Advanced Algorithm
	def getValidMoves(self):
		tempEnpassantPossible = self.enpassantPossible
		moves = []
		self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
		if self.whiteToMove:
			kingRow = self.whiteKingLocation[0]
			kingCol = self.whiteKingLocation[1]
		else:
			kingRow = self.blackKingLocation[0]
			kingCol = self.blackKingLocation[1]
		if self.inCheck: # ()
			if len(self.checks) == 1: # Only 1 check, block check, or move king
				moves = self.getAllPossibleMoves()
				# To block a check you must move a piece into one of the squares between the enemy piece and king
				check = self.checks[0] # Check Information
				checkRow = check[0]
				checkCol = check[1]
				pieceChecking = self.board[checkRow][checkCol] # Enemy piece causing the check
				validSquares = [] # Squares that pieces can move to
				# If knight, must capture knight or move king, other piece block
				if pieceChecking[1] == 'N':
					validSquares = [(checkRow, checkCol)]
				else:
					for i in range(1, 8):
						validSquare = (kingRow + check[2] * i, kingCol + check[3] * i) # check[2] and check[3] are the check directions
						validSquares.append(validSquare)
						if validSquare[0] == checkRow and validSquare[1] == checkCol: # Once you get to piece and checks
							break
				# Get rid of any moves that don't block check or move king
				for i in range(len(moves) - 1, -1, -1): # iterate through backwards
					if moves[i].pieceMoved[1] != 'K': # move doesn't move King so it must block or capture
						if not (moves[i].endRow, moves[i].endCol) in validSquares: # Move doesn't block check or capture piece
							moves.remove(moves[i])
			else: # Double check, king has to move
				self.getKingMoves(kingRow, kingCol, moves)
		else: # Not in check so all moves are fine
			moves = self.getAllPossibleMoves()
		self.enpassantPossible = tempEnpassantPossible

	# Naive Algorithm

	# def getValidMoves(self):
	# 	# Generate all possible moves
	# 	moves = self.getAllPossibleMoves()
	# 	# For each move, make the move
	# 	for i in range(len(moves)-1, -1, -1): # Iterate backwards to avoid bug
	# 		self.makeMove(moves[i])
	# 		# Generate all opponent moves
	# 		# For each opponent move, see if they attack your king
	# 		self.whiteToMove = not self.whiteToMove
	# 		if self.inCheck():
	# 			moves.remove(moves[i]) # If they do, not a valid move
	# 		self.whiteToMove = not self.whiteToMove
	# 		self.undoMove()
	# 	if len(moves) == 0: # Checkmate or Stalemate
	# 		if self.inCheck():
	# 			self.checkMate = True
	# 		else: self.staleMate = True
	# 	else:
	# 		self.checkMate = False
	# 		self.staleMate = False		
	# 	return moves

	def checkForPinsAndChecks(self):
		pins = [] # Squares where the allied pinned piece is and direction pinned from
		checks = [] # Squares where enemy is applying check
		inCheck = False
		if self.whiteToMove:
			enemyColor = 'b'
			allyColor = 'w'
			startRow = self.whiteKingLocation[0]
			startCol = self.whiteKingLocation[1]
		else:
			enemyColor = 'w'
			allyColor = 'b'
			startRow = self.blackKingLocation[0]
			startCol = self.blackKingLocation[1]
		# Check outward from king for pins and checks, keep track of pins
		directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
		for j in range(len(directions)):
			d = directions[j]
			possiblePin = () # Reset possible pins
			for i in range(1, 8):
				endRow = startRow + d[0] * i
				endCol = startCol + d[1] * i
				if 0 <= endRow < 8 and 0 <= endCol < 8:
					endPiece = self.board[endRow][endCol]
					if endPiece[0] == allyColor and endPiece[1] != 'K': 
						if possiblePin == (): # 1st allied piece could be pinned
							possiblePin = (endRow, endCol, d[0], d[1])
						else: # 2nd allied piece so no pin or check possible in this direction
							break
					elif endPiece[0] == enemyColor:
						type = endPiece[1]
						if (0 <= j <= 3 and type == 'R') or \
							(4 <= j <= 7 and type == 'B') or \
							(i == 1 and type == 'P' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
							(type == 'Q') or (i == 1 and type == 'K'):
							if possiblePin == (): # No piece blocking so check
								inCheck = True
								checks.append((endRow, endCol, d[0], d[1]))
								break
							else: # Piece blocking so pin
								pins.append(possiblePin)
								break
						else: # Enemy piece not applying check
							break
			else: # Off board
				break
		# Check for knight checks
		knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
		for m in knightMoves:
			endRow = startRow + m[0]
			endCol = startCol + m[1]
			if 0 <= endRow < 8 and 0 <= endCol < 8:
				endPiece = self.board[endRow][endCol]
				if endPiece[0] == enemyColor and endPiece[1] == 'N': # Enemy knight attacking  king
					inCheck = True
					checks.append((endRow, endCol, m[0], m[1]))
		return inCheck, pins, checks

	'''
	Determine if current player in check
	'''
	def inCheck(self):
		if self.whiteToMove:
			return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
		else:
			return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

	'''
	Determine if the enemy can attack square (r, c)
	'''
	def squareUnderAttack(self, r, c):
		self.whiteToMove = not self.whiteToMove # Switch to opponent turn
		oppMoves = self.getAllPossibleMoves()
		self.whiteToMove = not self.whiteToMove # Switch turns back
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
				if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
					piece = self.board[r][c][1]
					self.moveFunctions[piece](r, c, moves) # Call appropriate move function for each piece type
		return moves

	'''
	Get all the Pawn moves at row, column and add these moves to the list
	'''
	def getPawnMoves(self, r, c, moves):
		piecePinned = False
		pinDirection = ()
		for i in range(len(self.pins)-1, -1, -1):
			if self.pins[i][0] == r and self.pins[i][1] ==c:
				piecePinned = True
				pinDirection = (self.pins[i][2], self.pins[i][3])
				self.pins.remove(self.pins[i])
				break

		if self.whiteToMove: # White Pawn moves
			if self.board[r-1][c] == '--': # 1 square pawn advance
				if not piecePinned or pinDirection == (-1, 0):
					moves.append(Move((r , c), (r-1, c), self.board))
					if r == 6 and self.board[r-2][c] == '--': # 2 square pawn advance
						moves.append(Move((r , c), (r-2, c), self.board))
			# Captures
			if c-1 >= 0: # Capture to the left
				if self.board[r-1][c-1][0] == 'b': # Enemy piece to capture
					if not piecePinned or pinDirection == (-1, -1):
						moves.append(Move((r , c), (r-1, c-1), self.board))
				elif (r-1, c-1) == self.isEnpassantMove:
						moves.append(Move((r , c), (r-1, c-1), self.board, isEnpassantMove=True))

			if c+1 <= 7: # Capture to the right
				if self.board[r-1][c+1][0] == 'b': # Enemy piece to capture
					if not piecePinned or pinDirection == (-1, 1):
						moves.append(Move((r , c), (r-1, c+1), self.board))
				elif (r-1, c+1) == self.isEnpassantMove:
						moves.append(Move((r , c), (r-1, c+1), self.board, isEnpassantMove=True))
		else:
			# Black Pawn moves
			if self.board[r+1][c] == '--': # 1 square pawn advance
				if not piecePinned or pinDirection == (1, 0):
					moves.append(Move((r , c), (r+1, c), self.board))
					if r == 1 and self.board[r+2][c] == '--': # 2 square pawn advance
						moves.append(Move((r , c), (r+2, c), self.board))
			# Captures
			if c-1 >= 0: # Capture to the left
				if self.board[r+1][c-1][0] == 'w': # Enemy piece to capture
					if not piecePinned or pinDirection == (1, -1):
						moves.append(Move((r , c), (r+1, c-1), self.board))
				elif (r+1, c-1) == self.isEnpassantMove:
						moves.append(Move((r , c), (r+1, c-1), self.board, isEnpassantMove=True))
			if c+1 <= 7: # Capture to the right
				if self.board[r+1][c+1][0] == 'w': # Enemy piece to capture
					if not piecePinned or pinDirection == (1, 1):
						moves.append(Move((r , c), (r+1, c+1), self.board))
				elif (r+1, c+1) == self.isEnpassantMove:
						moves.append(Move((r , c), (r+1, c+1), self.board, isEnpassantMove=True))

	'''
	Get all the Rook moves at row, column and add these moves to the list
	'''
	def getRookMoves(self, r, c, moves):
		piecePinned = False
		pinDirection = ()
		for i in range(len(self.pins)-1, -1, -1):
			if self.pins[i][0] == r and self.pins[i][1] == c:
				piecePinned = True
				pinDirection = (self.pins[i][2], self.pins[i][3])
				if self.board[r][c][1] != 'Q': # cant remove queen from pin on rook moves, only removes it on bishop moves
					self.pins.remove(self.pins[i])
				break
		directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
		enemyColor = 'b' if self.whiteToMove else 'w'
		for d in directions:
			for i in range(1, 8):
				endRow = r + d[0] * i
				endCol = c + d[1] * i
				if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
					if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
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
		piecePinned = False
		for i in range(len(self.pins)-1, -1, -1):
			if self.pins[i][0] == r and self.pins[i][1] == c:
				piecePinned = True
				self.pins.remove(self.pins[i])
				break
		knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
		allyColor = 'w' if self.whiteToMove else 'b'
		for m in knightMoves:
			endRow = r + m[0]
			endCol = c + m[1]
			if 0 <= endRow < 8 and 0 <= endCol < 8:
				if not piecePinned:
					endPiece = self.board[endRow][endCol]
					if endPiece[0] != allyColor: # Not an ally piece (empty or enemy color)
						moves.append(Move((r, c), (endRow, endCol), self.board))
			
	'''
	Get all the Bishop moves at row, column and add these moves to the list
	'''
	def getBishopMoves(self, r, c, moves):
		piecePinned = False
		pinDirection = ()
		for i in range(len(self.pins)-1, -1, -1):
			if self.pins[i][0] == r and self.pins[i][1] == c:
				piecePinned = True
				pinDirection = (self.pins[i][2], self.pins[i][3])
				self.pins.remove(self.pins[i])
				break
		directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
		enemyColor = 'b' if self.whiteToMove else 'w'
		for d in directions:
			for i in range(1, 8):
				endRow = r + d[0] * i
				endCol = c + d[1] * i
				if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
					if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
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
		rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
		colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
		allyColor = 'w' if self.whiteToMove else 'b'
		for i in range(8):
			endRow = r + rowMoves[i]
			endCol = c + colMoves[i]
			if 0 <= endRow < 8 and 0 <= endCol < 8:
				endPiece = self.board[endRow][endCol]
				if endPiece[0] != allyColor: # Not an ally (empty or enemy piece)
					# Place king on end square and check for checks					
					if allyColor == 'w':
						self.whiteKingLocation = (endRow, endCol)
					else:
						self.blackKingLocation = (endRow, endCol)
					inCheck, pins, checks = self.checkForPinsAndChecks()
					if not inCheck:
						moves.append(Move((r, c), endRow, endCol), (self.board))
					# Place king back on original location
					if allyColor == 'w':
						self.whiteKingLocation = (r, c)
					else:
						self.blackKingLocation = (r, c)

class Move():
	# Maps keys to values
	# key: value
	ranksToRows = {'1': 7, '2': 6, '3': 5, '4': 4,
					'5': 3, '6': 2, '7': 1, '8': 0}
	rowToRanks = {v: k for k, v in ranksToRows.items()}
	filesToCols = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
					'e': 4, 'f': 5, 'g': 6, 'h': 7}
	colsToFiles = {v: k for k, v in filesToCols.items()}

	def __init__(self, startSq, endSq, board, isEnpassantMove=False:
		self.startRow = startSq[0]
		self.startCol = startSq[1]
		self.endRow = endSq[0]
		self.endCol = endSq[1]
		self.pieceMoved = board[self.startRow][self.startCol]
		self.pieceCaptured = board[self.endRow][self.endCol]
		# Pawn promotion
		self.isPawnPromotion = (self.pieceMoved == 'wP' and self.endRow == 0) or (self.pieceMoved == 'bP' and self.endRow == 7)
		# En Passant
		self.isEnpassantMove = isEnpassantMove
		if self.isEnpassantMove:
			self.pieceCaptured = 'wP' if self.pieceMoved == 'bP' else 'bP'

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

