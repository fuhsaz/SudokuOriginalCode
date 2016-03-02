from __future__ import print_function
import random
import copy

class Cell(object):
	"""
	row_index = 0
	col_index = 0
	box_index = 0
	box_location = 0
		# Will indicate where in a box the cell is, to save the time of searching the
		# whole puzzle for other cells in the same box
		# [1 2 3]
		# [4 5 6]
		# [7 8 9]
	val = 0
	possible = []
	notPossible = []
	cellID = 0
	branch = False
	guessVal = 0
	guessAt = 0
	toRemove = False
	keep = True
	"""
	def __init__(self, val, x, y, newID):
		self.val = val
		self.row_index = y
		self.col_index = x
		self.cellID = newID
		self.branch = False
		self.keep = True
		# figure out which box it's in
		if 0 <= y <= 2:
			if 0 <= x <= 2:
				self.box_index = 0
			elif 3 <= x <= 5:
				self.box_index = 1
			else:
				self.box_index = 2
		elif 3 <= y <= 5:
			if 0 <= x <= 2:
				self.box_index = 3
			elif 3 <= x <= 5:
				self.box_index = 4
			else:
				self.box_index = 5
		else:
			if 0 <= x <= 2:
				self.box_index = 6
			elif 3 <= x <= 5:
				self.box_index = 7
			else:
				self.box_index = 8

		# Assign a box location to each cell
		if   (x == 0 or x == 3 or x == 6) and (y == 0 or y == 3 or y == 6):
			self.box_location = 1
		elif (x == 1 or x == 4 or x == 7) and (y == 0 or y == 3 or y == 6):
			self.box_location = 2
		elif (x == 2 or x == 5 or x == 8) and (y == 0 or y == 3 or y == 6):
			self.box_location = 3
		elif (x == 0 or x == 3 or x == 6) and (y == 1 or y == 4 or y == 7):
			self.box_location = 4
		elif (x == 1 or x == 4 or x == 7) and (y == 1 or y == 4 or y == 7):
			self.box_location = 5
		elif (x == 2 or x == 5 or x == 8) and (y == 1 or y == 4 or y == 7):
			self.box_location = 6
		elif (x == 0 or x == 3 or x == 6) and (y == 2 or y == 5 or y == 8):
			self.box_location = 7
		elif (x == 1 or x == 4 or x == 7) and (y == 2 or y == 5 or y == 8):
			self.box_location = 8
		elif (x == 2 or x == 5 or x == 8) and (y == 2 or y == 5 or y == 8):
			self.box_location = 9	
		self.possible = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		self.notPossible = []

	# GETTERS
	def getVal(self):
		return self.val
	def getRow(self):
		return self.row_index
	def getCol(self):
		return self.col_index
	def getBox(self):
		return self.box_index
	def getBoxLoc(self):
		return self.box_location
	def getID(self):
		return self.cellID
	def getPossible(self):
		return self.possible
	def getNotPossible(self):
		return self.notPossible
	def getGuessAt(self):
		return self.guessAt
	def isBranch(self):
		return self.branch
	def shouldRemove(self):
		return self.toRemove
	def shouldKeep(self):
		return self.keep

	# SETTERS (If applicable)
	def setVal(self, newVal):
		self.val = newVal
	def makeBranch(self, truefalse):
		self.branch = truefalse
	def setGuessVal(self, val):
		self.guessVal = val
	def setGuessAt(self, val):
		self.guessAt = val
	def setNotPossible(self, val):
		self.notPossible = val
	def setRemove(self, val):
		self.toRemove = val
	def setPossible(self, val):
		self.possible = val
	def setKeep(self, val):
		self.keep = val

	# Remove a value from the possible list
	def eliminate(self, valToRemove):
		possible = self.possible
		if valToRemove in self.possible:
			self.possible.remove(valToRemove)

	# Add a bad guess to the not possible list
	def addToNotPossible(self, val):
		if not val in self.notPossible:
			self.notPossible.append(val)
		if val in self.possible:
			self.possible.remove(val)

	# Reset the possible values for this cell
	def resetPossible(self):
		newPossible = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		self.possible = list(newPossible)
		#("possible  set to",self.possible)
		#print("notPossible list",self.notPossible)
		listOfRemoved = []
		for each in self.notPossible:
			if each in self.possible:
				self.possible.remove(each)
				listOfRemoved.append(each)
		#print("removed         ",listOfRemoved)
		#print("final possible  ",self.possible)

	# Check if has been set
	def isEmpty(self):
		return self.val == 0

	# Check how long the guess list was before this was added to it (aka its position in the list)
	def getGuessLen(self):
		return self.guessLen

class Sudoku(object):
	# A list to hold the 9x9 cells of the puzzle
	cells = []
	# A list of cells filled in after the program had to guess for a box. If the guess was wrong, all the
	# Cells in this list will get reset and the cell at index 0 will have its current value added to its
	# notPossible list
	complete = []

	# Constructor
	def __init__(self):
		curID = 0
		for y in range(0, 9):
			col = []
			for x in range(0,9):
				col.append(Cell(0, x, y, curID))
				curID += 1
			self.cells.append(col)

	# Set the value of a cell
	def set(self, val, x, y):
		self.cells[y][x].setVal(val)

	# Set the value of a cell at a (x,y) coordinate, then update the possible lists of all affected cells
	def setUpdate(self, val, x, y):
		self.cells[y][x].setVal(val)
		self.update(self.cells[y][x], val)

	# Set the value of a cell and update the possible lists of all affected cells
	def setUpdateCell(self, cell, val):
		cell.setVal(val)
		self.update(cell, val)

	# Reset the possibles of all cells, then update them again, adding the value of the wrong guess 
	# To the cell's list of not possibles
	def reset(self):
		cells = self.getCells()
		for each in cells:
			each.resetPossible()

	def get(self, x, y):
		return self.cells[y][x]

	# Display the puzzle
	def display(self):
		yCount = 0
		print("-------------------")
		for y in self.cells:
			string = "| "
			xCount = 0
			for x in y:
				#string += str(len(x.getPossible()))
				string += str(x.getVal())
				xCount += 1
				if xCount == 3 or xCount == 6:
					string += " | "
			string += " |"
			print (string)
			yCount += 1
			if yCount == 3 or yCount == 6:
				print("|-----------------|")
		print("-------------------")
	def displayMore(self):
		yCount = 0
		print("------------------- -------------------")
		for y in self.cells:
			string = "| "
			xCount = 0
			for x in y:
				#string += str(len(x.getPossible()))
				string += str(x.getVal())
				xCount += 1
				if xCount == 3 or xCount == 6:
					string += " | "
			string += " | | "
			xCount = 0
			for x in y:
				if x.isEmpty():
					string += str(len(x.possible))
				else:
					string += " "
				xCount += 1
				if xCount == 3 or xCount == 6:
					string += " | "
			string += " |"
			print (string)
			yCount += 1
			if yCount == 3 or yCount == 6:
				print("|-----------------| |-----------------|")
		print("------------------- -------------------")
	# Each time a cell is given a value, no other cells in that row, col or box can have that
	# value, so this will check those and remove the value from their possible lists
	def update(self, cell, val):
		thisRow = cell.getRow()
		thisCol = cell.getCol()
		thisBox = cell.getBox()
		val = val

		rowList = self.returnRow(cell)
		colList = self.returnCol(cell)
		boxList = self.returnBox(cell)

		for each in rowList:
			each.eliminate(val)
		for each in colList:
			each.eliminate(val)
		for each in boxList:
			each.eliminate(val)
	def updateAll(self):
		cells = self.getCells()
		for aCell in cells:
			val = aCell.getVal()
			self.update(aCell, val)
	def resetAllPossibles(self):
		allCells = self.getCells()
		for eachCell in allCells:
			eachCell.resetPossible()
	def getCells(self):
		cells = []
		for each in self.cells:
			for each2 in each:
				cells.append(each2)
		return cells

	# Return a list of the cells in the same box as the given cell
	def returnBox(self, cell):
		box_location = cell.getBoxLoc()
		x = cell.getCol()
		y = cell.getRow()
		theBox = []
		if box_location == 1:
			theBox.append(self.get(x, y))
			theBox.append(self.get(x+1, y))
			theBox.append(self.get(x+2, y))
			theBox.append(self.get(x, y+1))
			theBox.append(self.get(x+1, y+1))
			theBox.append(self.get(x+2, y+1))
			theBox.append(self.get(x, y+2))
			theBox.append(self.get(x+1, y+2))
			theBox.append(self.get(x+2, y+2))
		elif box_location == 2:
			theBox.append(self.get(x-1, y))
			theBox.append(self.get(x, y))
			theBox.append(self.get(x+1, y))
			theBox.append(self.get(x-1, y+1))
			theBox.append(self.get(x, y+1))
			theBox.append(self.get(x+1, y+1))
			theBox.append(self.get(x-1, y+2))
			theBox.append(self.get(x, y+2))
			theBox.append(self.get(x+1, y+2))
		elif box_location == 3:
			theBox.append(self.get(x-2, y))
			theBox.append(self.get(x-1, y))
			theBox.append(self.get(x, y))
			theBox.append(self.get(x-2, y+1))
			theBox.append(self.get(x-1, y+1))
			theBox.append(self.get(x, y+1))
			theBox.append(self.get(x-2, y+2))
			theBox.append(self.get(x-1, y+2))
			theBox.append(self.get(x, y+2))
		elif box_location == 4:
			theBox.append(self.get(x, y-1))
			theBox.append(self.get(x+1, y-1))
			theBox.append(self.get(x+2, y-1))
			theBox.append(self.get(x, y))
			theBox.append(self.get(x+1, y))
			theBox.append(self.get(x+2, y))
			theBox.append(self.get(x, y+1))
			theBox.append(self.get(x+1, y+1))
			theBox.append(self.get(x+2, y+1))
		elif box_location == 5:
			theBox.append(self.get(x-1, y-1))
			theBox.append(self.get(x, y-1))
			theBox.append(self.get(x+1, y-1))
			theBox.append(self.get(x-1, y))
			theBox.append(self.get(x, y))
			theBox.append(self.get(x+1, y))
			theBox.append(self.get(x-1, y+1))
			theBox.append(self.get(x, y+1))
			theBox.append(self.get(x+1, y+1))
		elif box_location == 6:
			theBox.append(self.get(x-2, y-1))
			theBox.append(self.get(x-1, y-1))
			theBox.append(self.get(x, y-1))
			theBox.append(self.get(x-2, y))
			theBox.append(self.get(x-1, y))
			theBox.append(self.get(x, y))
			theBox.append(self.get(x-2, y+1))
			theBox.append(self.get(x-1, y+1))
			theBox.append(self.get(x, y+1))
		elif box_location == 7:
			theBox.append(self.get(x, y-2))
			theBox.append(self.get(x+1, y-2))
			theBox.append(self.get(x+2, y-2))
			theBox.append(self.get(x, y-1))
			theBox.append(self.get(x+1, y-1))
			theBox.append(self.get(x+2, y-1))
			theBox.append(self.get(x, y))
			theBox.append(self.get(x+1, y))
			theBox.append(self.get(x+2, y))
		elif box_location == 8:
			theBox.append(self.get(x-1, y-2))
			theBox.append(self.get(x, y-2))
			theBox.append(self.get(x+1, y-2))
			theBox.append(self.get(x-1, y-1))
			theBox.append(self.get(x, y-1))
			theBox.append(self.get(x+1, y-1))
			theBox.append(self.get(x-1, y))
			theBox.append(self.get(x, y))
			theBox.append(self.get(x+1, y))
		elif box_location == 9:
			theBox.append(self.get(x-2, y-2))
			theBox.append(self.get(x-1, y-2))
			theBox.append(self.get(x, y-2))
			theBox.append(self.get(x-2, y-1))
			theBox.append(self.get(x-1, y-1))
			theBox.append(self.get(x, y-1))
			theBox.append(self.get(x-2, y))
			theBox.append(self.get(x-1, y))
			theBox.append(self.get(x, y))
		return theBox
	# Return a list of the cells in the same row as the given cell
	def returnRow(self, cell):
		cellRow = cell.getRow()
		rowList = []
		for i in range(0,9):
			rowList.append(self.cells[cellRow][i])
		return rowList
	# Return a list of the cells in the same column as the given cell
	def returnCol(self, cell):
		cellCol = cell.getCol()
		colList = []
		for i in range(0,9):
			colList.append(self.cells[i][cellCol])
		return colList

	# The same methods, but take an index instead of a cell
	def returnBoxIndex(self, index):
		#find the coordinates of the top-left cell of the box, then find the other cells from there
		if index == 0:
			x = 0
			y = 0
		elif index == 1:
			x = 3
			y = 0
		elif index == 2:
			x = 6
			y = 0
		elif index == 3:
			x = 0
			y = 3
		elif index == 4:
			x = 3
			y = 3
		elif index == 5:
			x = 6
			y = 3
		elif index == 6:
			x = 0
			y = 6
		elif index == 7:
			x = 3
			y = 6
		elif index == 8:
			x = 6
			y = 6

		boxList = []
		boxList.append(self.get(x, y))
		boxList.append(self.get(x, y+1))
		boxList.append(self.get(x, y+2))
		boxList.append(self.get(x+1, y))
		boxList.append(self.get(x+1, y+1))
		boxList.append(self.get(x+1, y+2))
		boxList.append(self.get(x+2, y))
		boxList.append(self.get(x+2, y+1))
		boxList.append(self.get(x+2, y+2))
		
		return boxList			
	def returnRowIndex(self, index):
		cellRow = index
		rowList = []
		for i in range(0,9):
			rowList.append(self.cells[cellRow][i])
		return rowList
	def returnColIndex(self, index):
		cellCol = index
		colList = []
		for i in range(0,9):
			colList.append(self.cells[i][cellCol])
		return colList

	# Check the row of the given cell to make sure no rules are broken
	def checkRow(self, cell):
		row_index = cell.getRow()
		check = [0,0,0,0,0,0,0,0,0,0]
		for i in range(0, 9):
			cur = self.cells[row_index][i].getVal()
			if check[cur] == 0:
				check[cur] += 1;
			elif check[cur] == 1:
				return False
		return True
	# Check the column of the given cell to make sure no rules are broken
	def checkCol(self, cell):
		col_index = cell.getCol()
		check = [0,0,0,0,0,0,0,0,0,0]
		for i in range(0, 9):
			cur = self.cells[i][col_index].getVal()
			if check[cur] == 0:
				check[cur] += 1;
			elif check[cur] == 1:
				return False
		return True		
	# Check the box of the given cell to make sure no rules are broken
	def checkBox(self, cell):
		boxList = self.returnBox(cell)
		check = [0,0,0,0,0,0,0,0,0,0]
		found = []
		for each in boxList:
			found.append(each.getVal())
		count = 0
		for each in found:	
			if check[each] == 0:
				check[each] += 1
			elif check[each] == 1:
				return False
		return True
		
	# Methods to get the availability of a row, col, or box
	def rowAv(self, cell):
		possible = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		rowList = self.returnRow(cell)
		for each in rowList:
			val = each.getVal()
			if not val == 0:
				possible.remove(val)
		return possible
	def colAv(self, cell):
		possible = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		colList = self.returnCol(cell)
		for each in colList:
			val = each.getVal()
			if not val == 0:
				possible.remove(val)
		return possible
	def boxAv(self, cell):
		possible = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		boxList = self.returnBox(cell)
		for each in boxList:
			val = each.getVal()
			if not val == 0:
				possible.remove(val)
		return possible

	# Return a list of the cells in the puzzle that don't currently have a value, sorted by the
	# number of values they could possibly have
	def getEmpty(self):
		allCells = self.getCells()
		empty = []
		for each in allCells:
			#print(each)
			if each.getVal() == 0:
				empty.append(each)
		newList = sorted(empty, key=lambda x: len(x.possible))
		return newList
	def getFilled(self):
		allCells = self.getCells()
		filled = list([])
		for each in allCells:
			if not each.getVal == 0:
				filled.append(each)
		return filled
	# Return a list of the empty cells in the box of the given cell
	def getEmptyBox(self, cell):
		boxList = self.returnBox(cell)
		emptyList = []
		for each in boxList:
			if each.getVal() == 0:
				emptyList.append(each)
		return emptyList

	# Return a list of the empty cells in the row of the given cell	
	def getEmptyRow(self, cell):
		rowList = self.returnRow(cell)
		emptyList = []
		for each in rowList:
			if each.getVal() == 0:
				emptyList.append(each)
		return emptyList

	# Return a list of the empty cells in the column of the given cell
	def getEmptyCol(self, cell):
		colList = self.returnRow(cell)
		emptyList = []
		for each in colList:
			if each.getVal() == 0:
				emptyList.append(each)
		return emptyList

	# Set of methods to check whether any numbers in the row, box, or column can only be placed in 
	# one empty cell, if so, returns that cell, if not, returns false
	def findOnlySpotRow(self, rowIndex):
		numbers = [0,0,0,0,0,0,0,0,0,0]
		row = self.returnRowIndex(rowIndex)
		#print("searching row",rowIndex)
		count = 1
		for each in row:
			if not each.isEmpty():
				count += 1
				continue
			possible = each.getPossible()
			#print("row ", each.getRow()," col ", each.getCol(), possible)
			for pos in possible:
				numbers[pos] += 1
			count += 1
			#print(numbers)
		theNum = 0
		for i in range(1,10):
			#print("checking ", i)
			if numbers[i] == 1:
				#print ("found")
				return i
		return 0	
	def findOnlySpotCol(self, colIndex):
		numbers = [0,0,0,0,0,0,0,0,0,0]
		col = self.returnColIndex(colIndex)
		count = 1
		#print("searching col",colIndex)
		for each in col:
			if not each.isEmpty():
				count += 1
				continue
			possible = each.getPossible()
			#print("row ", each.getRow()," col ", each.getCol(), possible)
			for pos in possible:
				numbers[pos] += 1
			count += 1
		theNum = 0
		for i in range(1,10):
			#print("checking ", i)
			if numbers[i] == 1:
				#print ("found")
				return i
		return 0
	def findOnlySpotBox(self, boxIndex):
		numbers = [0,0,0,0,0,0,0,0,0,0]
		box = self.returnBoxIndex(boxIndex)
		count = 1
		#print("searching box",boxIndex)
		for each in box:
			if not each.isEmpty():
				count += 1
				continue
			possible = each.getPossible()
			#print("row ", each.getRow()," col ", each.getCol(), possible)
			for pos in possible:
				numbers[pos] += 1
			count += 1
		theNum = 0
		for i in range(1,10):
			#print("checking ", i)
			if numbers[i] == 1:
				#print ("found")
				return i
		return 0
		
	# Turns out I need to make a solver first, and before that I need to read in a puzzle to solve
	def getNew(self, fileName):
		f = open(fileName, 'r')
		count = 0
		cells = self.getCells()
		for line in f:
			for i in range(0,81):
				if line[i] == '.':
					continue
				else:
					val = int(line[i])
					self.setUpdateCell(cells[i], val)
			break
	def readWholeFile(self, fileName):
		pass
	def remove(self, cell):
		return cell.shouldRemove()
	"""
	Now a method to solve it, with backtracking. Will keep a list of 'unsure' cells in case a guess has
	to be made, and then they can be cleared if it runs into a snag. The current value of the cell at
	the top of the list will be removed from its list of possibles
	Steps:
		1) Get a list of all the empty cells, sorted by the length of their possible list. If one or more cells
			have only one possible value, fill that value in and update the puzzle
		2) If none of the cells have only 1 possible value, fill a list with any cases where a certain 
			number can only be put in one cell of a row, column, or box. If any of these are found, put them in
			one at a time and update the list

	"""

	def solve(self):
		solved = False
		while not solved:
			self.displayMore()
			#raw_input()
			cellList = self.getEmpty()
			backtrack = False
			# First, see if the list of empty cells is empty. If so, the puzzle might
			# be solved, check all rows, cols and boxes
			if not backtrack:
				if len(cellList) == 0:
					# Then the puzzle is solved, provided it passes the checks
					for i in range(0, 9):
						check = self.checkRow(self.get(i, 0))
						if check == False:
							break
					if check == False:
						# Need to backtrack
						backtrack = True
					if not backtrack:
						for i in range(0, 9):
							check = self.checkCol(self.get(0, i))
							if check == False:
								break
						if check == False:
							# Need to backtrack
							backtrack = True
					if not backtrack:
						for i in range(0, 3):
							ind1 = i*3
							for j in range(0,3):
								ind2 = j*3
								check = self.checkBox(self.get(ind1, ind2))
								if check == False:
									break
							if check == False:
								break
					if check == False:
						# Need to backtrack
						backtrack = True
					else:
						solved = True
						continue

			# Otherwise, check the length of the possible list of the first cell in
			# the list of empty cells. 
			cur = cellList[0]
			# If it is 0, there was a wrong guess, and need to backtrack
			if len(cur.getPossible()) == 0 or backtrack:
		# Begin Backtracking
				#print("missed a guess")
				listOfEmpty = self.getEmpty()
				"""
				for every in listOfEmpty:
					print(every.possible)
				print()
				"""
				# In order to backtrack, go backwards through the list of 
				# completed cells. At each one, check whether it is a (and the
				# most recent) branch, where a guess was made
				#print("looking at completed list")
				for each in reversed(self.complete):
					# Replace old iteration variables with new ones
					curPossible = list(each.getPossible())
					curVal = each.getVal()
					curNotPossible = list(each.getNotPossible())

					curRow = each.getRow()
					curCol = each.getCol()
					curIsBranch = each.isBranch()

					#print("looking at row",curRow,"col",curCol,"val",curVal, "poss",curPossible)

					# If the cell is not a branch, reset its value, reset its list
					# of not possible (in case a guess was wrong only because of
					# an earlier wrong guess), and remove it from the list of 
					# completed cells

					#print("inspecting: branch",curIsBranch,"num possible",len(curPossible))
					if not curIsBranch:
						#print("decided not branch")
						each.setVal(0)
						newNotPossible = []
						each.notPossible = list(newNotPossible)
						# mark the current cell to be removed from the list
						each.setKeep(False)
						eachNewVal = each.getVal()
						#print("new: row",curRow,"col",curCol,"val:",each.getVal())
						#print()

					# If the cell is a branch, there are two cases:
					else:
					# a) If, after updating its list of not possible values,
					#		there are no remaining values, then the guess that 
					#		can be corrected is further down the line. Treat this
					#		cell like the other nonbranches, as well as setting
					#		isBranch to False.
						#print("-----------FOUND BRANCH------------")
						# First need to make sure the branch doesn't have any possibles
						# AFTER the cells have been removed
						#print("current possible",curPossible)
						if not curVal in curNotPossible:
							curNotPossible.append(curVal)

						self.resetAllPossibles()

						for x in curNotPossible:
							if x in each.possible:
								each.possible.remove(x)
							if not x in each.notPossible:
								each.notPossible.append(x)

						#print("reset possible",list(each.getPossible()))

						self.updateAll()

						newPossible = list(each.getPossible())
						#print("new possible",newPossible)

						if len(newPossible) == 0:
							#print("decided no possibility branch, continuing")
							#print()
							each.setVal(0)
							each.setNotPossible(list([]))
							# mark the current cell to be removed from the list
							each.setKeep(False)
							each.makeBranch(False)

						else:
						# b) The cell is a branch with at 1+ numbers as possible
						#		values. This is the target of the backtrack, where 
						#		something went wrong and can be fixed. Get the wrongly
						#		guessed value and store it in the list of notPossible
						#		values, then update the list of possible values and 
						#		select the next one as the new value. The possible
						# 		lists of all cells will be reset next, so that isn't
						#		necessary now.
							#print("decided target branch")
							#print()

							if not curVal in each.notPossible:
								each.notPossible.append(curVal)
							if curVal in each.possible:
								each.possible.remove(curVal)
							#print("added", curVal,"to not possible, making it",each.getNotPossible())
							#print("removed", curVal,"from possible, making it",each.getPossible())

							newVal = each.getPossible()[0]
							# If the possible list NOW only has 1 possible value, this
							# cell isn't a branch any more
							self.setUpdateCell(each,newVal)
							if len(each.possible) == 0:
								#print("setting to",newVal,"(not a guess)")
								each.makeBranch(False)
							else:
								#print("guessing",newVal,"from",newPossible)
								each.makeBranch(True)
							# Need to stop looping back through the completed list
							#print()
							break

				# Now that it's done iterating back through the complete list,
				# it's safe to remove the cells that had their values reset from
				# the list of completed cells	
				#print("current # complete",len(self.complete))	
				newComplete = list([])
				for each in self.complete:
					curRow = each.getRow()
					curCol = each.getCol()
					if each.shouldKeep():
						newComplete.append(each)
					else: 
						pass
						#print("removing cell at row",curRow,"col",curCol)
				self.complete = list(newComplete)

				#print("new # complete",len(self.complete))

				self.resetAllPossibles()
				self.updateAll()
				# And return to the top of the loop, after setting backtrack to False
				backtrack = False
				continue
		#End backtracking

			# If it is 1, there is only one possible value for the cell. Fill the cell
			# in, add it to the completed list cells, update the table, and return
			# to the top of the loop
			if len(cur.getPossible()) == 1:
				newVal = cur.getPossible()[0]
				newPossible  = list(cur.getPossible())
				newRow = cur.getRow()
				newCol = cur.getCol()
				self.setUpdateCell(cur, newVal)
				self.complete.append(cur)
				#cur.setPossible([ret])
				# Confirm that this cell labelled not as a branch(guess)
				cur.makeBranch(False)
				#print("found a cell")
				#print("row", newRow,"col",newCol,"only possible value was",newPossible)
				continue
			#print("no unique cells found")
			# Next, check each row, then each column, then each box for a number
			# that can only go in one cell. If one is found, fill in that cell,
			# update the puzzle, add the cell to the completed list, and return
			# to the top of the loop
			found = False
			ret = 0
			foundRow = 0
			foundCol = 0
			# Check rows
			for i in range(0, 9):
				ret = self.findOnlySpotRow(i)
				if ret != 0:
					row = self.returnRowIndex(i)
					for each in row:
						#print("looking for ",ret, "in the possibles", each.getPossible())
						if ret in each.getPossible() and each.isEmpty():
							#print("found")
							foundPossible = list(each.getPossible())
							self.setUpdateCell(each, ret)
							self.complete.append(each)
							#each.setPossible([ret])
							# This cell is not a guess
							each.makeBranch(False)
							found = True
							foundRow = each.getRow()
							foundCol = each.getCol()
							
							break
						elif ret in each.getPossible():
							pass
							#print("not empty")
						else:
							pass
							#print("not in possible")
				if found:
					break
			# If one was found, return to the top of the loop
			if found:
				#print("found a row")
				#print("row", foundRow,"col",foundCol,"only possible value was",ret)
				#print("possibles for that cell",foundPossible)
				continue
			#print("no unique rows found")
			# Check cols
			foundRow = 0
			foundCol = 0
			for i in range(0, 9):
				ret = self.findOnlySpotCol(i)
				if ret != 0:
					col = self.returnColIndex(i)
					for each in col:
						if ret in each.getPossible() and each.isEmpty():
							foundPossible = list(each.getPossible())
							self.setUpdateCell(each, ret)
							self.complete.append(each)
							#each.setPossible([ret])
							# This cell is not a guess
							each.makeBranch(False)
							found = True
							foundRow = each.getRow()
							foundCol = each.getCol()
							break
				if found:
					break
			# If one was found, return to the top of the loop
			if found:
				#print("found a col")
				#print("row", foundRow,"col",foundCol,"only possible value was",ret)
				#print("possibles for that cell",foundPossible)
				continue
			#print("no unique cols found")
			# Check boxes
			foundRow = 0
			foundCol = 0
			for i in range(0, 9):
				ret = self.findOnlySpotBox(i)
				if ret != 0:
					box = self.returnBoxIndex(i)
					for each in box:
						if ret in each.getPossible() and each.isEmpty():
							foundPossible = list(each.getPossible())
							self.setUpdateCell(each, ret)
							self.complete.append(each)
							#each.setPossible([ret])
							# This cell is not a guess
							each.makeBranch(False)
							found = True
							foundRow = each.getRow()
							foundCol = each.getCol()
							break
				if found:
					break
			# If one was found, return to the top of the list
			if found:
				#print("found a box")
				#print("row", foundRow,"col",foundCol,"only possible value was",ret)
				#print("possibles for that cell",foundPossible)
				continue
			#print("no unique boxes found")

			# Finally, if no certain cells or numbers are found, we have to guess,
			# preferably on the cell with the fewest possible values, already 
			# stored in 'cur'
			guessVal = cur.getPossible()[0]
			guessPossible = list(cur.getPossible())
			guessRow = cur.getRow()
			guessCol = cur.getCol()
			# This cell is a guess
			cur.makeBranch(True)
			self.setUpdateCell(cur, guessVal)
			#print("guessing",guessVal,"at row",guessRow,"col",guessCol,"possibleGuesses",guessPossible)
			self.complete.append(cur)
		self.display()

	def getHardness(self):
		
		solved = False
		uniqueCells = []
		uniqueNumbers = []
		guesses = []
		while not solved:
			print("getting hardness")
			#self.displayMore()
			#raw_input()
			cellList = self.getEmpty()
			backtrack = False
			# First, see if the list of empty cells is empty. If so, the puzzle might
			# be solved, check all rows, cols and boxes
			if not backtrack:
				if len(cellList) == 0:
					# Then the puzzle is solved, provided it passes the checks
					for i in range(0, 9):
						check = self.checkRow(self.get(i, 0))
						if check == False:
							break
					if check == False:
						# Need to backtrack
						backtrack = True
					if not backtrack:
						for i in range(0, 9):
							check = self.checkCol(self.get(0, i))
							if check == False:
								break
						if check == False:
							# Need to backtrack
							backtrack = True
					if not backtrack:
						for i in range(0, 3):
							ind1 = i*3
							for j in range(0,3):
								ind2 = j*3
								check = self.checkBox(self.get(ind1, ind2))
								if check == False:
									break
							if check == False:
								break
					if check == False:
						# Need to backtrack
						backtrack = True
					else:
						solved = True
						continue

			# Otherwise, check the length of the possible list of the first cell in
			# the list of empty cells. 
			cur = cellList[0]
			curID = cur.getID()
			# If it is 0, there was a wrong guess, and need to backtrack
			if len(cur.getPossible()) == 0 or backtrack:
		# Begin Backtracking
				#print("missed a guess")
				listOfEmpty = self.getEmpty()
				for every in listOfEmpty:
					pass
					#print(every.possible)
				#print()

				# In order to backtrack, go backwards through the list of 
				# completed cells. At each one, check whether it is a (and the
				# most recent) branch, where a guess was made
				#print("looking at completed list")
				for each in reversed(self.complete):
					# Replace old iteration variables with new ones
					curPossible = list(each.getPossible())
					curVal = each.getVal()
					curNotPossible = list(each.getNotPossible())

					curRow = each.getRow()
					curCol = each.getCol()
					curIsBranch = each.isBranch()

					#print("looking at row",curRow,"col",curCol,"val",curVal, "poss",curPossible)

					# If the cell is not a branch, reset its value, reset its list
					# of not possible (in case a guess was wrong only because of
					# an earlier wrong guess), and remove it from the list of 
					# completed cells

					#print("inspecting: branch",curIsBranch,"num possible",len(curPossible))
					if not curIsBranch:
						#print("decided not branch")
						each.setVal(0)
						newNotPossible = []
						each.notPossible = list(newNotPossible)
						# mark the current cell to be removed from the list
						each.setKeep(False)
						if each in uniqueCells:
							uniqueCells.remove(each)
						if each in uniqueNumbers:
							uniqueNumbers.remove(each)
						eachNewVal = each.getVal()
						#print("new: row",curRow,"col",curCol,"val:",each.getVal())
						#print()

					# If the cell is a branch, there are two cases:
					else:
					# a) If, after updating its list of not possible values,
					#		there are no remaining values, then the guess that 
					#		can be corrected is further down the line. Treat this
					#		cell like the other nonbranches, as well as setting
					#		isBranch to False.
						#print("-----------FOUND BRANCH------------")
						# First need to make sure the branch doesn't have any possibles
						# AFTER the cells have been removed
						#print("current possible",curPossible)
						if not curVal in curNotPossible:
							curNotPossible.append(curVal)

						self.resetAllPossibles()

						for x in curNotPossible:
							if x in each.possible:
								each.possible.remove(x)
							if not x in each.notPossible:
								each.notPossible.append(x)

						#print("reset possible",list(each.getPossible()))

						self.updateAll()

						newPossible = list(each.getPossible())
						#print("new possible",newPossible)

						if len(newPossible) == 0:
							#print("decided no possibility branch, continuing")
							#print()
							each.setVal(0)
							each.setNotPossible(list([]))
							# mark the current cell to be removed from the list
							each.setKeep(False)
							each.makeBranch(False)

						else:
						# b) The cell is a branch with at 1+ numbers as possible
						#		values. This is the target of the backtrack, where 
						#		something went wrong and can be fixed. Get the wrongly
						#		guessed value and store it in the list of notPossible
						#		values, then update the list of possible values and 
						#		select the next one as the new value. The possible
						# 		lists of all cells will be reset next, so that isn't
						#		necessary now.
							#print("decided target branch")
							#print()

							if not curVal in each.notPossible:
								each.notPossible.append(curVal)
							if curVal in each.possible:
								each.possible.remove(curVal)
							#print("added", curVal,"to not possible, making it",each.getNotPossible())
							#print("removed", curVal,"from possible, making it",each.getPossible())

							newVal = each.getPossible()[0]
							# If the possible list NOW only has 1 possible value, this
							# cell isn't a branch any more
							self.setUpdateCell(each,newVal)
							if len(each.possible) == 0:
								#print("setting to",newVal,"(not a guess)")
								each.makeBranch(False)
							else:
								#print("guessing",newVal,"from",newPossible)
								each.makeBranch(True)
							# Need to stop looping back through the completed list
							#print()
							break

				# Now that it's done iterating back through the complete list,
				# it's safe to remove the cells that had their values reset from
				# the list of completed cells	
				#print("current # complete",len(self.complete))	
				newComplete = list([])
				for each in self.complete:
					curRow = each.getRow()
					curCol = each.getCol()
					if each.shouldKeep():
						newComplete.append(each)
					else:
						pass 
						#print("removing cell at row",curRow,"col",curCol)
				self.complete = list(newComplete)

				#print("new # complete",len(self.complete))

				self.resetAllPossibles()
				self.updateAll()
				# And return to the top of the loop, after setting backtrack to False
				backtrack = False
				continue
		#End backtracking

			# If it is 1, there is only one possible value for the cell. Fill the cell
			# in, add it to the completed list cells, update the table, and return
			# to the top of the loop
			if len(cur.getPossible()) == 1:
				newVal = cur.getPossible()[0]
				newPossible  = list(cur.getPossible())
				newRow = cur.getRow()
				newCol = cur.getCol()
				self.setUpdateCell(cur, newVal)
				self.complete.append(cur)
				#cur.setPossible([ret])
				# Confirm that this cell labelled not as a branch(guess)
				cur.makeBranch(False)
				#print("found a cell")
				#print("row", newRow,"col",newCol,"only possible value was",newPossible)
				uniqueCells.append(curID)
				if curID in guesses:
					guesses.remove(curID)
				continue
			#print("no unique cells found")
			# Next, check each row, then each column, then each box for a number
			# that can only go in one cell. If one is found, fill in that cell,
			# update the puzzle, add the cell to the completed list, and return
			# to the top of the loop
			found = False
			ret = 0
			foundRow = 0
			foundCol = 0
			# Check rows
			for i in range(0, 9):
				ret = self.findOnlySpotRow(i)
				if ret != 0:
					row = self.returnRowIndex(i)
					for each in row:
						#print("looking for ",ret, "in the possibles", each.getPossible())
						if ret in each.getPossible() and each.isEmpty():
							#print("found")
							foundPossible = list(each.getPossible())
							self.setUpdateCell(each, ret)
							self.complete.append(each)
							#each.setPossible([ret])
							# This cell is not a guess
							each.makeBranch(False)
							found = True
							foundRow = each.getRow()
							foundCol = each.getCol()
							
							break
						elif ret in each.getPossible():
							pass
							#print("not empty")
						else:
							pass
							#print("not in possible")
				if found:
					break
			# If one was found, return to the top of the loop
			if found:
				#print("found a row")
				#print("row", foundRow,"col",foundCol,"only possible value was",ret)
				#print("possibles for that cell",foundPossible)
				uniqueNumbers.append(curID)
				if curID in guesses:
					guesses.remove(curID)
				continue
			#print("no unique rows found")
			# Check cols
			foundRow = 0
			foundCol = 0
			for i in range(0, 9):
				ret = self.findOnlySpotCol(i)
				if ret != 0:
					col = self.returnColIndex(i)
					for each in col:
						if ret in each.getPossible() and each.isEmpty():
							foundPossible = list(each.getPossible())
							self.setUpdateCell(each, ret)
							self.complete.append(each)
							#each.setPossible([ret])
							# This cell is not a guess
							each.makeBranch(False)
							found = True
							foundRow = each.getRow()
							foundCol = each.getCol()
							break
				if found:
					break
			# If one was found, return to the top of the loop
			if found:
				#print("found a col")
				#print("row", foundRow,"col",foundCol,"only possible value was",ret)
				#print("possibles for that cell",foundPossible)
				uniqueNumbers.append(curID)
				if curID in guesses:
					guesses.remove(curID)
				continue
			#print("no unique cols found")
			# Check boxes
			foundRow = 0
			foundCol = 0
			for i in range(0, 9):
				ret = self.findOnlySpotBox(i)
				if ret != 0:
					box = self.returnBoxIndex(i)
					for each in box:
						if ret in each.getPossible() and each.isEmpty():
							foundPossible = list(each.getPossible())
							self.setUpdateCell(each, ret)
							self.complete.append(each)
							#each.setPossible([ret])
							# This cell is not a guess
							each.makeBranch(False)
							found = True
							foundRow = each.getRow()
							foundCol = each.getCol()
							break
				if found:
					break
			# If one was found, return to the top of the list
			if found:
				#print("found a box")
				#print("row", foundRow,"col",foundCol,"only possible value was",ret)
				#print("possibles for that cell",foundPossible)
				uniqueNumbers.append(curID)
				if curID in guesses:
					guesses.remove(curID)
				continue
			#print("no unique boxes found")

			# Finally, if no certain cells or numbers are found, we have to guess,
			# preferably on the cell with the fewest possible values, already 
			# stored in 'cur'
			guessVal = cur.getPossible()[0]
			guessPossible = list(cur.getPossible())
			guessRow = cur.getRow()
			guessCol = cur.getCol()
			# This cell is a guess
			cur.makeBranch(True)
			self.setUpdateCell(cur, guessVal)
			#print("guessing",guessVal,"at row",guessRow,"col",guessCol,"possibleGuesses",guessPossible)
			self.complete.append(cur)
			guesses.append(curID)
		rets = [len(uniqueCells), len(uniqueNumbers), len(guesses)]
		return rets

# Take in a complete sudoku, and a difficulty argument.
# Select an index in the sudoku and remove that cell (set value back to 0)
# Then check the hardness of the puzzle resulting from the removal. If it didn't exceed
# The desired difficulty, continue, if it did, undo that step and try another space
def generate(s, diff):
	hardEnough = False
	while not hardEnough:

		base = s
		numCells = 0
		numNumbers = 0
		minNumbers = 0
		numGuesses = 0
		minGuesses = 0
		finalNumClues = random.randint(25, 31)
		tooHardCount = 0
		listOfX = []
		listOfY = []
		filled = base.getFilled()
		# Set difficulty limits. What I'm thinking is that finding a cell where only one number is possible
		# is the easiest 'operation' one can perform on a sudoku. Someone doing easy puzzles should know how
		# to do that. A harder operation is finding, among a row, column, or box, a number that can only go
		# in one cell, even if that cell has other possiblities (What I've been calling a 'unique number'). The 
		# hardest operation is making a guess, so only 'hard' puzzles will allow that.

		# The finished puzzle should probably have between 25 and 31 clues remaining
		# Alternatively, if it generates a puzzle that is too hard 5 times in a row, just return the puzzle
		difficulty = []
		diff = diff.lower()
		if diff=='easy':
		# Easy: Unlimited unique cells
		#		Few unique numbers
		#		No guesses
			difficulty = [100, 4, 0]
		elif diff == 'medium':
		# Med:	Unlimited unique cells
		#		More unique numbers
		#		Maybe one guess
			difficulty = [100, 10, 1]
			minNumbers = 4
		elif diff == 'hard':
		# Hard:	Unlimited unique cells
		#		Unlimited unique numbers
		#		A few guesses
			difficulty = [100, 100, 3]
			minNumbers = 10
			minGuesses = 1
		else:
			print("Invalid difficulty")
			return

	

		tooHardSetPoint = 0
		done = False
		failsafe = 0

		while not done:
			print("loop just continued, done:",done)
			for i in range(0, len(listOfX)):
				base.set(0, listOfX[i], listOfY[i])
			base.display()
			#raw_input()
			numRemaining = len(filled)
			print ("num remaining",numRemaining)
			print("check 1")
			if numRemaining < finalNumClues or tooHardCount >= 5:
				print("leaving the loop")
				#raw_input()
				print("check 2")
				done = True
				print("done just set to true, done:",done)

				continue
				
			if numRemaining <= 30:
				tooHardSetPoint = 30-numRemaining
				print("check 3")
			print("check 7")
			minimum = 0
			maximum = len(filled)-1
			indexToRemove = random.randint(minimum, maximum)

			targetCell = filled[indexToRemove]
			targX = targetCell.getCol()
			targY = targetCell.getRow()
			targetOldVal = targetCell.getVal()
			targetCell.setVal(0)
			filled.remove(targetCell)
			print("check 4")
			base.resetAllPossibles()
			base.updateAll()
			print("check 5")
			rets = base.getHardness()
			print(rets)
			tooHard = False
			print("check 6")
			for i in range(0,3):
				print ("comparing ret",rets[i],"to the difficulty limit",difficulty[i])
				if rets[i] > difficulty[i]:
					tooHard = True
			#raw_input()
			if tooHard:
				# If difficulty is exceeded, try again with a different spot
				print("too hard (ret:",rets,")")
				targetCell.setVal(targetOldVal)
				filled.append(targetCell)
				tooHardCount += 1
				#print("too hard count", tooHardCount)
				continue
			else:
				# Else update the original and continue
				listOfX.append(targX)
				listOfY.append(targY)
				tooHardCount = tooHardSetPoint
				#print("too hard count reset", tooHardCount)
	
		for i in range(0, len(listOfX)):
			base.set(0, listOfX[i], listOfY[i])
		base.resetAllPossibles()
		base.updateAll()
		rets = base.getHardness()
		if rets[1] >= minNumbers and rets[2] >= minGuesses and rets[1] <= difficulty[1]and rets[2] <= difficulty[2]:
			hardEnough = True
			print(rets)
		else:
			print("have to start over.")
			base.solve()
			filled = list(base.getFilled())
	for i in range(0, len(listOfX)):
		base.set(0, listOfX[i], listOfY[i])
	base.resetAllPossibles()
	base.updateAll()	
	base.display()

		
		

"""
s = Sudoku()
s.setUpdate(4, 4, 4)
s.display()
s.updateAll()
s.display()
s.resetAllPossibles()
s.display()
s.updateAll()
s.display()
"""


su = Sudoku()
su.getNew('TestPuzzles1.txt')
su.display()
#raw_input()
su.solve()

generate(su, 'easy')
"""
s = Sudoku()
#s.setUpdate(4, 4, 4)
s.display()
raw_input()
s.solve()
"""
"""
su.display()
su.generate()
su.display()
"""
"""
rowList = su.returnCol(su.get(0,0))
for each in rowList:
	print(each.cellID)

colList = su.returnCol(su.get(0,0))
for each in colList:
	print(each.cellID)


boxList = su.returnBox(su.get(8,2))
for each in boxList:
	print(each.cellID)
"""

"""
# Put 1-9 in a box
su.set(1, 0, 0)
su.set(2, 1, 0)
su.set(3, 2, 0)
su.set(4, 0, 1)
su.set(5, 1, 1)
su.set(6, 2, 1)
su.set(7, 0, 2)
su.set(8, 1, 2)
su.set(9, 2, 2)
su.display()
print(su.checkBox(su.get(0, 0)))
"""

"""
# Put 1-9 in a row
su.set(1, 0, 0)
su.set(2, 1, 0)
su.set(3, 2, 0)
su.set(4, 3, 0)
su.set(5, 4, 0)
su.set(6, 5, 0)
su.set(7, 6, 0)
su.set(8, 7, 0)
su.set(9, 8, 0)
su.display()
print(su.checkRow(su.get(0, 0)))
"""

"""
# Put 1-9 in a column
su.set(1, 0, 0)
su.set(2, 0, 1)
su.set(3, 0, 2)
su.set(4, 0, 3)
su.set(5, 0, 4)
su.set(6, 0, 5)
su.set(7, 0, 6)
su.set(9, 0, 7)
su.set(9, 0, 8)
su.display()
print(su.checkCol(su.get(0, 0)))
"""

