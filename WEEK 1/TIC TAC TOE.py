import random

# Initialize the board
board = [" " for _ in range(9)]

def print_board():
    print()
    for i in range(3):
        print(" | ".join(board[i*3:(i+1)*3]))
        if i < 2:
            print("-" * 5)
    print()

def check_winner(player):
    win_states = [
        [0,1,2], [3,4,5], [6,7,8],  # rows
        [0,3,6], [1,4,7], [2,5,8],  # columns
        [0,4,8], [2,4,6]            # diagonals
    ]
    for state in win_states:
        if all(board[i] == player for i in state):
            return True
    return False

def is_full():
    return " " not in board

def computer_move():
    available = [i for i in range(9) if board[i] == " "]
    move = random.choice(available)   # Pick random free cell
    board[move] = "X"

def user_move():
    while True:
        try:
            pos = int(input("Enter your move (1-9): ")) - 1
            if pos < 0 or pos > 8 or board[pos] != " ":
                print("Invalid move. Try again.")
            else:
                board[pos] = "O"
                break
        except ValueError:
            print("Please enter a valid number (1-9).")

def play():
    print("Welcome to Tic-Tac-Toe! (Computer: X, You: O)")
    print("Positions are numbered as follows:")
    print("1 | 2 | 3")
    print("---------")
    print("4 | 5 | 6")
    print("---------")
    print("7 | 8 | 9")
    print_board()

    while True:
        
        user_move()
        print_board()
        if check_winner("O"):
            print("You win! 🎉")
            break
        if is_full():
            print("It's a draw!")
            break

        computer_move()
        print("Computer played:")
        print_board()
        if check_winner("X"):
            print("Computer wins! 💻")
            break
        if is_full():
            print("It's a draw!")
            break

play()
