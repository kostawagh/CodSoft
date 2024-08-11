import tkinter as tk
from tkinter import messagebox
import gameEngine as game

class TicTacToe:
    def __init__(self):
        # Create the main window
        self.root = tk.Tk()
        self.root.geometry("400x400")  
        self.root.configure(bg='lightgray')
        self.root.title("Tic-Tac-Toe")
        self.load_images()  # Load images
        self.createGrid()

    def load_images(self):
        # Load images
        self.x_image = tk.PhotoImage(file='x.png')
        self.o_image = tk.PhotoImage(file='o.png')
        self.empty_image = tk.PhotoImage(file='-.png')  # Placeholder image

    def createGrid(self):
        # Frame for the 3x3 grid
        grid_frame = tk.Frame(self.root)
        grid_frame.pack(pady=10)  

        # 3x3 grid of buttons
        self.gridCells = [[None for _ in range(3)] for _ in range(3)]
        for row in range(3):
            for col in range(3):
                self.gridCells[row][col] = tk.Button(grid_frame, width=100, height=100, image=self.empty_image, command=lambda r=row, c=col: self.buttonClick(r, c))
                self.gridCells[row][col].grid(row=row, column=col)  

        # ControlFrame
        controlFrame = tk.Frame(self.root)
        controlFrame.pack(pady=10)

        # Menu to choose mode/difficulty
        modeOptions = ["Easy AI", "Medium AI", "Hard AI"]
        self.selectedMode = tk.StringVar(self.root)
        self.selectedMode.set(modeOptions[0])  # Easy is default
        modeMenu = tk.OptionMenu(controlFrame, self.selectedMode, *modeOptions, command=self.lockMode)
        modeMenu.grid(row=1, column=0, padx=10)  

        # Help button
        helpButton = tk.Button(controlFrame, text="Help", command=self.showHelp)
        helpButton.grid(row=1, column=1, padx=10)  # Place in the second column

        # Reset button
        resetButton = tk.Button(controlFrame, text="Reset", command=self.resetGame)
        resetButton.grid(row=1, column=2, padx=10)  # Place in the third column

        self.gameMode = "Easy AI"  # Default Mode
        self.symbol = 'X'  # Human always plays as X
        self.current_player = 'X'
        self.grid = [[' ' for _ in range(3)] for _ in range(3)]
        self.gameActive = True

    def buttonClick(self, row, col):
        if self.gameActive and self.grid[row][col] == ' ':  # if game is active and cell is empty
            if self.current_player == self.symbol:  # if it is human's turn
                self.grid[row][col] = self.current_player  # update in record
                if self.current_player == 'X':
                    self.gridCells[row][col].config(image=self.x_image)  # update visually on grid
                elif self.current_player == 'O':
                    self.gridCells[row][col].config(image=self.o_image)  # update visually on grid

                # Check conditions now
                if game.checkWin(self.grid, self.current_player):
                    messagebox.showinfo("Game Over", f"Player {self.current_player} Wins!")
                    self.gameActive = False
                elif game.checkDraw(self.grid):
                    messagebox.showinfo("Game Over", "It's a Draw!")
                    self.gameActive = False
                else:
                    self.current_player = 'O' if self.current_player == 'X' else 'X'
                    if self.current_player == 'O':
                        self.make_ai_move()

    def make_ai_move(self):
        if self.gameMode == 'Easy AI':
            row, col = game.ezAImove(self.grid)
        elif self.gameMode == 'Medium AI':
            row, col = game.mediumAImove(self.grid)
        elif self.gameMode == 'Hard AI':
            row, col = game.minimaxMove(self.grid)
        else:
            return

        self.grid[row][col] = 'O'
        self.gridCells[row][col].config(image=self.o_image)
        if game.checkWin(self.grid, 'O'):
            messagebox.showinfo("Game Over", "AI Wins!")
            self.gameActive = False
        elif game.checkDraw(self.grid):
            messagebox.showinfo("Game Over", "It's a Draw!")
            self.gameActive = False
        else:
            self.current_player = 'X'

    def resetGame(self):
        # Reset the game state
        self.current_player = 'X'
        self.grid = [[' ' for _ in range(3)] for _ in range(3)]
        self.gameActive = True
        for row in range(3):
            for col in range(3):
                self.gridCells[row][col].config(image=self.empty_image)

    def lockMode(self, value):
        self.gameMode = value
        self.resetGame()  # Reset the game when difficulty changes


    def showHelp(self):
        help = ("""Tic-Tac-Toe v1.3 \nDeveloper: Kaustubh Wagh\n\n
Game Instructions:\n
- The game is played on a 3x3 grid.
- You always play as 'X', and the AI plays as 'O'.
- Click on an empty cell to make your move.
- The game ends when one player gets three in a row (horizontally, vertically, or diagonally), 
-The game ends in a draw if the grid is full and no one has won.
- Use the difficulty menu to select the AI's difficulty level.
- Click 'Reset' to start a new game at any time.""")
        messagebox.showinfo("Help", help)


def main():
    app = TicTacToe()
    app.root.mainloop()

if __name__ == "__main__":
    main()
