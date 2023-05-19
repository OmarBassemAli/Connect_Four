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
