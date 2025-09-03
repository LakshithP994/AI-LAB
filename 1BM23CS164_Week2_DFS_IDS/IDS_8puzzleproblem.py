# Import necessary libraries
from collections import deque

# Define the dimensions of the puzzle
N = 3

# Structure to store a state of the puzzle
class PuzzleState:
    def __init__(self, board, x, y, depth):
        self.board = board
        self.x = x
        self.y = y
        self.depth = depth

# Possible moves: Left, Right, Up, Down
row = [0, 0, -1, 1]
col = [-1, 1, 0, 0]

# Function to check if a given state is the goal state
def is_goal_state(board):
    goal = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]
    return board == goal

# Function to check if a move is valid
def is_valid(x, y):
    return 0 <= x < N and 0 <= y < N

# Function to print the board
def print_board(board):
    for row in board:
        print(' '.join(map(str, row)))
    print("--------")

# Iterative Deepening Depth-First Search to solve the 8-puzzle problem
def solve_puzzle_idfs(start, x, y):
    def dfs(curr_state, limit, visited):
        # If we exceed the limit, return False (no solution at this depth)
        if curr_state.depth > limit:
            return False
        
        # Print the current board
        print(f'Depth: {curr_state.depth}')
        print_board(curr_state.board)

        # Check if goal state is reached
        if is_goal_state(curr_state.board):
            print(f'Goal state reached at depth {curr_state.depth}')
            return True

        # Explore possible moves
        for i in range(4):
            new_x = curr_state.x + row[i]
            new_y = curr_state.y + col[i]

            if is_valid(new_x, new_y):
                new_board = [row[:] for row in curr_state.board]
                # Swap the tiles
                new_board[curr_state.x][curr_state.y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[curr_state.x][curr_state.y]

                # If this state has not been visited before, push to stack
                board_tuple = tuple(map(tuple, new_board))
                if board_tuple not in visited:
                    visited.add(board_tuple)
                    next_state = PuzzleState(new_board, new_x, new_y, curr_state.depth + 1)
                    
                    # Recursively call dfs for deeper depth
                    if dfs(next_state, limit, visited):
                        return True

        # If no solution is found at this depth
        return False

    # Start with depth limit from 0 and increase
    depth_limit = 0
    while True:
        visited = set()
        visited.add(tuple(map(tuple, start)))
        
        print(f"Trying with depth limit: {depth_limit}")
        
        # Start DFS from the initial state with the current depth limit
        if dfs(PuzzleState(start, x, y, 0), depth_limit, visited):
            break
        
        depth_limit += 1  # Increase the depth limit for the next iteration

    print('Solution found.')

# Driver Code
if __name__ == '__main__':
    start = [[2, 8, 3], [1, 6, 4], [7, 0, 5]]
    x, y = 1, 1

    print('Initial State:')
    print_board(start)

    solve_puzzle_idfs(start, x, y)
