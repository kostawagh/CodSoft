'''
Version 1.3
- added
- play as O

Version 1.2
-Included a medium difficulty
-Bug Fixes
-organised program better

'''

import random


# To Start a New Game
# game grid is a nested list (3x3 grid of empty spaces)
def newGame():
  global grid, current_player
  grid= [[' ' for _ in range(3)] for _ in range(3)]
  current_player = 'X'

#-----------------------------------------------------------------------------------------------
# GAME RULES
# checks if current player has 3 in a line
def checkWin(grid, currPlayer):
  # row check
  for row in range(3):      # check rows 0,1,2
    if all([cell == currPlayer for cell in grid[row]]):     # if all cells are currPlayer in the row
        return True

  # column check
  for col in range(3):      # check col 0,1,2
    if all([grid[row][col] == currPlayer for row in range(3)]):
      return True

  # first diagonal check
  if all([grid[n][n] == currPlayer for n in range(3)]):
    return True
    
  # other diagonal check
  if all([grid[n][2-n] == currPlayer for n in range(3)]):
    return True
  
  #otherwise: continue with game
  return False


# check if all cells are occupied
def checkDraw(grid):
  if all([cell != " " for row in grid for cell in row]):
    return True
  else:
    return False

#---------------------------------------------------------------------------------------------------
  
# AI Evaluation Engine - MiniMax   (maximize prob of winning, minimize prob of losing)

def minimax(grid, depth, is_maximizing):
    # Checking if Game Over- Evaluation
    if checkWin(grid, 'O'):           # if O won (AI)
      return 1
    if checkWin(grid, 'X'):           # if X won (Human)
      return -1
    if checkDraw(grid):
      return 0
    
    # MAXIMIZING CONDITION - AI MOVE
    if is_maximizing:
      bestScore = float('-inf')     # set to -infinity
      # checking all possible opponents moves (kinda looks into all future possiblities)
      for row in range(3):
        for col in range(3):
          if grid[row][col] == ' ':                 # checking if empty
            grid[row][col] = 'O'

            score = minimax(grid, depth+1, False)
            grid[row][col] = ' '                    # cleans up after checking all possibilities
            bestScore = max(score, bestScore)       # takes bigger value

      # return best score that AI can get on this turn
      return bestScore


    # MINIMIZING CONDTION- Opponent MOVE
    else:
      bestScore = float('inf')      # set to infinity
      # explored all possible next moves for the AI
      for row in range(3):
        for col in range(3):
          if grid[row][col] == ' ':                   # checking if empty
            grid[row][col] = 'X'

            score = minimax(grid, depth+1, True)      # sets to maximizing condtion (AI move incoming)
            grid[row][col] = ' '                      # cleans up after checking all possibilities
            bestScore = min(score, bestScore)         # takes smaller value

      return bestScore



# MOVE MAKER - HARD AI : MinimaxMove
def minimaxMove(grid):
  bestScore = float('-inf')
  move = (-1,-1)                        # initializing the move with place holder

  #check which is the best move for it
  for row in range(3):
    for col in range(3):
      if grid[row][col] == ' ':         # check if cell is empty
        grid[row][col] = 'O'

        score = minimax(grid,0,False)
        grid[row][col] = ' '            # cleans up after checking all possibilities

        # chooses a move and returns it
        if score > bestScore:
          bestScore = score
          move = (row,col)              # tuple to avoid change
      
  return move


#-------------------------------------------
# MOVE MAKER - EASY AI
def ezAImove(grid):
  empty_cells = [(row, col) for row in range(3) for col in range(3) if grid[row][col] == ' ']
  return random.choice(empty_cells)


#-------------------------------------------
# MOVE MAKER - MEDIUM AI
def mediumAImove(grid):
  prob = 0.7                    # 80% chance to use minimax, else random

  if random.random() <prob:     # gives a random value between 0 and 1
    return minimaxMove(grid)
  else:
    return ezAImove(grid)
