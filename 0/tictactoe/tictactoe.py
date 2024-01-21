"""
Tic Tac Toe Player
"""
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_cnt = 0
    o_cnt = 0
    for row in board:
        for cell in row:
            if cell == X:
                x_cnt += 1
            elif cell == O:
                o_cnt += 1

    return X if x_cnt == o_cnt else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    empty = set()
    for i in range(3):  # i: 0, 1, 2
        for j in range(3):
            if board[i][j] == EMPTY:
                empty.add((i, j))
    return empty


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # debug: board.copy() is only shallow copy
    new_board = copy.deepcopy(board)
    i, j = action
    if i not in range(3) or j not in range(3) or board[i][j] is not EMPTY:
        raise Exception("Invalid action: ({}, {})".format(i, j))
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check rows
    for row in board:
        if row[0] == row[1] == row[2] != EMPTY:
            return row[0]
    # check columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]
    # check diagonals
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    # check if board is full
    for row in board:
        for cell in row:
            if cell is EMPTY:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)
    if w == X:
        return 1
    elif w == O:
        return -1
    else:
        return 0


def max_optimal(board, alpha=-1, beta=1):
    """
    Returns best utility and action for maximizer(X)
    """
    # alpha-beta pruning
    # alpha/beta: the best value that max/minimizer can guarantee
    # over 20 times efficiency improvement in local test
    if terminal(board):
        return utility(board), None
    v = -1
    best_action = None
    for action in actions(board):
        tmp, _ = min_optimal(result(board, action), alpha, beta)
        if tmp > v:  # v = max(v, tmp)
            v = tmp
            best_action = action
        alpha = max(alpha, tmp)
        if alpha >= beta:
            break  # beta cut-off
    return v, best_action


def min_optimal(board, alpha=-1, beta=1):
    """
    Returns best utility and action for minimizer(O)
    """
    if terminal(board):
        return utility(board), None
    v = 1
    best_action = None
    for action in actions(board):
        tmp, _ = max_optimal(result(board, action), alpha, beta)
        if tmp < v:  # v = min(v, tmp)
            v = tmp
            best_action = action
        beta = min(beta, tmp)
        if alpha >= beta:
            break  # alpha cut-off
    return v, best_action


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    elif player(board) == X:
        return max_optimal(board)[1]
    else:
        return min_optimal(board)[1]
