import math
import random
import copy
import tkinter as tk

# default number of rows and columns
num_of_rows = 6
num_of_columns = 7

# create a board of 6*7 dimensions
def create_board():
    connect_4_board = []
    for i in range(num_of_rows):
        row = []
        for j in range(num_of_columns):
            row.append(0)
        connect_4_board.append(row)
    return connect_4_board

# put piece in specific row and column
def set_piece(connect_4_board, row, column, the_piece):
    connect_4_board[row][column] = the_piece

# checks if the top cell of the column is empty = the column is valid
def valid_column(connect_4_board, column):
    if connect_4_board[num_of_rows - 1][column] == 0:
        return True
    else:
        return False

# return first empty cell in a column
def return_empty_cell(connect_4_board, column):
    for row in range(num_of_rows):
        if connect_4_board[row][column] == 0:
            return row

# print board
def display_board(connect_4_board):
    for row in reversed(connect_4_board):
        print(row)

# checks if 4 adjacent cells contain the same piece (horizontal-vertical-diagonals)
def check_if_win(connect_4_board, the_piece):
    # Check horizontally
    for column in range(num_of_columns - 3):  # removes 3 columns from right
        for row in range(num_of_rows):
            if connect_4_board[row][column] == the_piece and connect_4_board[row][column + 1] == the_piece and connect_4_board[row][column + 2] == the_piece and connect_4_board[row][column + 3] == the_piece:
                return True
            # return true if 4 horizontal are same piece

    # Check vertically
    for column in range(num_of_columns):
        for row in range(num_of_rows - 3):  # remove 3 rows from top of the board
            if connect_4_board[row][column] == the_piece and connect_4_board[row + 1][column] == the_piece and connect_4_board[row + 2][column] == the_piece and connect_4_board[row + 3][column] == the_piece:
                return True
            # return true if 4 vertical are same piece

    # Check in diagonals
    for column in range(num_of_columns - 3):  # removes 3 columns from right
        for row in range(num_of_rows - 3):  # remove 3 rows from top of the board
            if connect_4_board[row][column] == the_piece and connect_4_board[row + 1][column + 1] == the_piece and connect_4_board[row + 2][column + 2] == the_piece and connect_4_board[row + 3][column + 3] == the_piece:
                return True
            # return true if 4 diagonal are same piece

    for column in range(num_of_columns - 3):  # removes 3 columns from right
        for row in range(3, num_of_rows):   # remove 3 rows from bottom
            if connect_4_board[row][column] == the_piece and connect_4_board[row - 1][column + 1] == the_piece and connect_4_board[row - 2][column + 2] == the_piece and connect_4_board[row - 3][column + 3] == the_piece:
                return True



# calculate the value of the whole board for each column by dividing the board to lists of 4 pieces and give each list value
# and sums the total values and return it
def calculate_board_value(connect_4_board, the_piece):
# create a list for the middle column and multiply the number of pieces in it by 3 to increase the value of the board
# to increase its value according to the number of pieces in the middle column

    value = 0
    middle_column = []
    for i in range(len(connect_4_board)):
        middle_column.append(int(connect_4_board[i][num_of_columns // 2]))

    num_of_middle = middle_column.count(the_piece)
    value += num_of_middle * 3

    # calculate the value horizontal by calculating each 4 cells next to each other horizontally
    for r in range(num_of_rows):
        row_array = [int(i) for i in connect_4_board[r]]

        for c in range(num_of_columns - 3):
            window = row_array[c:c + 4]
            value += calculate_list_of_4(window, the_piece)

    # calculate the value vertical by calculating each 4 cells next to each other vertically
    for c in range(num_of_columns):
        col_array = []
        for r in range(num_of_rows):
            col_array.append(int(connect_4_board[r][c]))

        for r in range(num_of_rows - 3):
            window = [col_array[r], col_array[r + 1], col_array[r + 2], col_array[r + 3]]
            value += calculate_list_of_4(window, the_piece)

    # calculate the value horizontal by calculating each 4 cells next to each other diagonally
    for r in range(num_of_rows - 3):
        for c in range(num_of_columns - 3):
            window = [connect_4_board[r + i][c + i] for i in range(4)]
            value += calculate_list_of_4(window, the_piece)

    for r in range(num_of_rows - 3):
        for c in range(num_of_columns - 3):
            window = [connect_4_board[r + 3 - i][c + i] for i in range(4)]
            value += calculate_list_of_4(window, the_piece)

    return value
# return the total value of the board

# calculate the value of 4 cells {List} next to each other according to number of pieces in them, the higher the number of pieces
# the higher the value

def calculate_list_of_4(list_of_4, the_piece):
    value = 0
    opposite_piece = 1
    if the_piece == 1:
        opposite_piece = 2

    if list_of_4.count(the_piece) == 4: # if list of 4 has 4 of the same piece
        value += 100  # increase value by 100
    elif list_of_4.count(the_piece) == 3 and list_of_4.count(0) == 1: # if list of 4 has 3 of same piece and one empty cell
        value += 5  # increase value by 5
    elif list_of_4.count(the_piece) == 2 and list_of_4.count(0) == 2: # if list of 4 has 2 of same piece and two empty cell
        value += 2  # increase value by 2
    if list_of_4.count(opposite_piece) == 3 and list_of_4.count(0) == 1: # if list of 4 has 3 of opponent piece and one empty cell
        value -= 4  # decrease value
    return value

# return the columns that are not full to the top
def get_available_columns(connect_4_board):
    available_columns = [] # list of available columns
    for column in range(num_of_columns):
        if valid_column(connect_4_board, column): # check if column is valid
            available_columns.append(column) # append the available column to the list
    return available_columns

# return a valid column
def choose_column(connect_4_board, the_piece):
    available_columns = get_available_columns(connect_4_board) # get all available columns in a list
    best_score = -999999999999  # best score is initially -99999999
    best_col = random.choice(available_columns)
    for col in available_columns:
        row = return_empty_cell(connect_4_board, col)  # return the first empty row in the column
        temp_board = copy.deepcopy(connect_4_board)  # make a copy of the board to try the pieces in
        set_piece(temp_board, row, col, the_piece) # put the piece in the board
        score = calculate_board_value(temp_board, the_piece) # calculate the total score of the board
        if score > best_score:  # if the score is higher than the best score, the new score is set as the best score
            best_score = score
            best_col = col
    return best_col
# return the column of the highest board score

# check if current board state is a win or a draw
def check_if_win_or_draw(connect_4_board):
    return check_if_win(connect_4_board, 1) or check_if_win(connect_4_board, 2) or len(get_available_columns(connect_4_board)) == 0

# minimax function return the best column according to minimax + alpha-beta pruning
def minimax(connect_4_board, the_depth, alpha_value, beta_value, max_player): # take board, depth, alpha, beta, max or min player as parameters
    available_columns = get_available_columns(connect_4_board) # get available columns of the board
    is_game_end = check_if_win_or_draw(connect_4_board) # check if game state is win or draw
    if the_depth == 0 or is_game_end:
        if is_game_end:
            if check_if_win(connect_4_board, 2): # check if AI player won
                return None, 100000000000000 # return a very high number to favor this column for AI
            elif check_if_win(connect_4_board, 1):  # check if computer won
                return None, -10000000000000 # return a very low number to favor this column for computer
            else: # Game is over, no more valid moves
                return None, 0
        else: # Depth is zero
            return None, calculate_board_value(connect_4_board, 2)
    if max_player: # if maximizing player is true
        value = -math.inf
        column = random.choice(available_columns)
        for col in available_columns: # iterate on all valid columns in the board
            row = return_empty_cell(connect_4_board, col) # return the first empty cell in the column
            b_copy = copy.deepcopy(connect_4_board) # make a copy of the board to try pieces in
            set_piece(b_copy, row, col, 2) # put piece in the board
            new_score = minimax(b_copy, the_depth - 1, alpha_value, beta_value, False)[1] # put the value in the new_score variable
            if new_score > value: # if new score is higher than value, set value to the new score
                value = new_score
                column = col
            alpha_value = max(alpha_value, value) # set alpha value to the bigger between alpha value and value
            if alpha_value >= beta_value: # if alpha value greater than beta,
                break                       #this is a move better than the beta player has found
                                            # so no need to complete searching and break the loop
        return column, value

    else:  # Min player
        value = math.inf
        column = random.choice(available_columns)
        for col in available_columns:  # iterate on all valid columns in the board
            row = return_empty_cell(connect_4_board, col) # return the first empty cell in the column
            b_copy = copy.deepcopy(connect_4_board) # make a copy of the board to try pieces in
            set_piece(b_copy, row, col, 1) # put piece in the board
            new_score = minimax(b_copy, the_depth - 1, alpha_value, beta_value, True)[1] # put the value in the new_score variable
            if new_score < value: # if new score is lower than value, set value to the new score
                value = new_score
                column = col
            beta_value = min(beta_value, value) # set beta value to the smaller between beta value and value
            if alpha_value >= beta_value: # if alpha value greater than beta,
                break                     #this is a move better than the beta player has found
        return column, value              # so no need to complete searching and break the loop


connect_4_board = create_board() # create board of specified dimensions
game_end = False # set game_end to false initially
turn = 0  # turn initially equals zero


depth = 0
def choose_difficulty():
    global depth # set depth as global variable
    difficulty = difficulty_var.get()
    if difficulty == 1: # if user chose easy, set depth to 2
        print("Easy")
        depth = 2
    elif difficulty == 2: # if user chose medium, set depth to 3
        print("Medium")
        depth = 3
    elif difficulty == 3: # if user chose hard, set depth to 5
        print("Hard")
        depth = 5

# Create a new window
window = tk.Tk()

# Set the window title
window.title("Choose Game Difficulty")

# Set the window size
window.geometry("500x300")

# Create a label to prompt the user for input
prompt_label = tk.Label(window, text="Choose a difficulty level:")
prompt_label.pack()

# Create a variable to store the selected difficulty level
difficulty_var = tk.IntVar()

# Create radio buttons for each difficulty level
easy_button = tk.Radiobutton(window, text="Easy", variable=difficulty_var, value=1)
easy_button.pack()

medium_button = tk.Radiobutton(window, text="Medium", variable=difficulty_var, value=2)
medium_button.pack()

hard_button = tk.Radiobutton(window, text="Hard", variable=difficulty_var, value=3)
hard_button.pack()

# Create a button to submit the selected difficulty
submit_button = tk.Button(window, text="Submit", command=choose_difficulty)
submit_button.pack()

# Run the window
window.mainloop()


while not game_end:
    display_board(connect_4_board)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    # Computer Input
    if turn == 0:
        column = choose_column(connect_4_board, 1)  # computer input without minimax
        if valid_column(connect_4_board, column):  # if column not full to top
            row = return_empty_cell(connect_4_board, column)  # get first empty cell in the row
            set_piece(connect_4_board, row, column, 1)  # put the piece in the board

            if check_if_win(connect_4_board, 1):  # check if the current board is a win state
                game_end = True  # set the game end to exit the while loop
                display_board(connect_4_board)  # show the full board
                print("Computer Victory")

    # AI Input
    else:
        column, minimax_score = minimax(connect_4_board, depth, -math.inf, math.inf, True)  # Ai input using minimax + alpha beta
        if valid_column(connect_4_board, column):  # if column not full to top
            row = return_empty_cell(connect_4_board, column)  # get first empty cell in the row
            set_piece(connect_4_board, row, column, 2)  # put the piece in the board

            if check_if_win(connect_4_board, 2):  # check if the current board is a win state
                game_end = True  # set the game end to exit the while loop
                display_board(connect_4_board)  # show the full board
                print("AI Victory")

    turn += 1
    turn = turn % 2
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")



