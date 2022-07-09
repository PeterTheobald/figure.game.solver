# figure.game.solver.py 2022 @ControlAltPete

board_strings = [ 'PPWPW', 'GGGPG', 'GGWGP', 'PPGPY', 'GPGGG']
max_moves = 8

def main(board_strings):
    board = init_board(board_strings)
    winning_moves = solve(board, 1)
    if winning_moves:
        print('Solution: ', winning_moves)
    else:
        print('Impossible\n')

def init_board( board_strings):
    # convert board to 2D array, easier to work with
    board = [[board_strings[row][col] for col in range(len(board_strings[0]))] for row in range(len(board_strings))]
    return board

def solve(board, move_num):
    # tries all valid moves on this board
    # returns empty list or sequence of winning moves, each move is list of cells to remove as [ (color, row, col), ... ]
    if move_num>max_moves:
        return []
    moves = find_moves(board)
    for move in moves:
        winning_moves = try_move( move, board, move_num)
        if winning_moves:
            return winning_moves
    return [] # no winning branches

def find_moves( board):
    # find orthogonally connected strings of same letters touching the bottom row
    # returns list of moves, each move is a list of cells (color, row, col) (first cell must be on bottom row)
    board2 = [row[:] for row in board] # deep copy
    moves=[]
    for col in range(0,len(board2[0])):
        move=add_with_neighbors( board2, len(board2)-1, col)
        if move:
            moves.append(move)
    return moves
    
def add_with_neighbors( board, row, col):
    # note this and recursive calls mutates board. must pass by reference
    color = board[row][col][0]
    if color == 'x' or color == ' ':
        return [] # already visited or empty
    cell = ( color, row, col)
    move = []
    board[row][col]='x'
    # add any matching neighbors
    if row>0 and board[row-1][col] == color:
        move += add_with_neighbors( board, row-1, col)
    if row<len(board)-1 and board[row+1][col] == color:
        move += add_with_neighbors( board, row+1, col)
    if col>0 and board[row][col-1] == color:
        move += add_with_neighbors( board, row, col-1)
    if col<len(board[0])-1 and board[row][col+1] == color:
        move += add_with_neighbors( board, row, col+1)
    move = [ cell ] + move # first cell on bottom row goes in front
    return move
    
def try_move( move, board, move_num):
    # 'click' the move, remove that cell and all connected cells
    # gravity move all cells over empty cells
    # recursively call solve on the new board
    board = update_board( move, board)
    if winning_board( board):
        return [move]
    moves = solve(board, move_num+1)
    if moves:
        return [move]+moves
    else:
        return []
    
def winning_board( board):
    winning = True
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] != ' ':
                winning = False
    return winning
    
def update_board( move, board):
    board2 = [row[:] for row in board] # deep copy
    # mark deleted cells
    for cell in move:
        board2[cell[1]][cell[2]] = 'x'
    # gravity fall cells above removed ones
    change=True
    while change: # repeat until no more cells fall
        change=False
        for row in range(len(board2)-1, 0, -1):
            for col in range(0, len(board2[0])):
                if board2[row][col] == 'x':
                    board2[row][col]=board2[row-1][col]
                    board2[row-1][col]='x'
                    change=True
        for col in range(0, len(board2[0])):
            if board2[0][col] == 'x':
                board2[0][col]=' '
                change=True
    return board2

main(board_strings)
