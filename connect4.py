import random
import math
import copy
board_width = 5
board_rows = 5
board = []
diff = ""
turn = 1
def agent():
    # random
    moves = {}
    if (diff == "random"):
        return random.randint(0, board_width) - 1
    elif (diff == "easy"):
        possible_states = []
        value = -math.inf
        best_cols = []
        bestmove = None
        for i in range(board_width):
            possible_states.append(make_move(board, i, 2)[0])
        print(possible_states)
        for x in possible_states:
            cscore = score_board(x, 2)
            if cscore > value:
                value = cscore
                best_cols = [possible_states.index(x)]
            elif cscore == value:
                best_cols.append(possible_states.index(x))
        print(f"bestcols = {best_cols}")
        return random.choice(best_cols), value
    elif diff == "medium":
        return minimax(board, 4, -math.inf, math.inf, True)
    elif diff == "hard": #me rn fr :weary:
        return minimax(board, 5, -math.inf, math.inf, True)

def minimax(board, depth, a, b, maxplayer):
    global turn #checking for end cases
    if depth == 0 or checkBoard(board):
        if checkBoard(board) and turn == 1:
            return (None, -100000023042034)
        elif checkBoard(board) and turn == 2:
            return (None, 1023990248927)
        else:
            if depth == 0: #depth is 0
                scor = (None, score_board(board, 2))
                return scor
    elif board[0].count(0) == 0:
        print("DRAW")
        #print(board)
        return (None, 0) #it's a draw
    possible_states = []
    possible_cols = []
    for i in range(board_width):
        moves = make_move(board, i, 2)
        if(moves):
            possible_states.append(moves[0])
            possible_cols.append(moves[1])

    if maxplayer: #ai
        value = -math.inf
        cols = [random.choice(possible_cols)]
        for c in possible_cols:
            newboard = make_move(board, c, 2)[0]
            n_score = minimax(newboard, depth-1, a, b, False)[1]
            #print(f"ai = {n_score}")
            if n_score > value: #if equal add to viable cols and randomly select one that works
                value = n_score
                #print(value)
                cols = [c]
            elif n_score == value:
                cols.append(c)
            a = max(a, value)
            if a >= b:
                break
        print(f"ai = {cols}")
        return random.choice(cols), value

    else: #player
        value = math.inf
        cols = [random.choice(possible_cols)]
        for c in possible_cols:
            newboard = make_move(board, c, 1)[0]
            n_score = minimax(newboard, depth-1, a, b, True)[1]
            #print(f"player = {n_score}")
            if n_score < value:
                value = n_score
                cols = [c]
            elif n_score == value:
                value = n_score
                #print(value)
                cols.append(c)
            b = min(b, value)
            if a >= b:
                break
        print(f"player = {cols}, score = {value}")
        return random.choice(cols), value

def score_window(window,plyr): #exclusively for use by the ai
    score = 0
    if plyr == 2:
        opp = 1
    else:
        opp = 2

    if window.count(plyr) == 4:
        score += 1000 #win
    elif window.count(plyr) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(plyr) == 2 == window.count(0):
        score += 2
    elif window.count(plyr) == 1 and window.count(0) == 3:
        score += 1

    if window.count(opp) == 3 and window.count(0) == 1:
        score -= 4
    elif window.count(opp) == 4:
        score -= 1000
    return score

def score_board(board, plyr):
    tscore = 0
    # sideways
    for i in board:
        for x in range(board_width - 3):
            window = [i[x],i[x + 1],i[x + 2],i[x + 3]]
            tscore += score_window(window, plyr)

    # upright
    for i in range(board_rows - 3):
        for x in range(board_width):
            window = [board[i][x], board[i + 1][x], board[i + 2][x], board[i + 3][x]]
            tscore += score_window(window, plyr)

    # diagonal down \
    for i in range(board_rows - 3):
        for x in range(board_width - 3):
            window = [board[i][x], board[i + 1][x + 1], board[i + 1][x + 1], board[i + 1][x + 1]]
            tscore += score_window(window, plyr)

    # diagonal up /
    for i in range(board_rows - 3):
        for x in range(board_width - 3):
            srcx = i+3
            srcy = x
            window = [board[srcx][srcy], board[srcx-1][srcy+1], board[srcx-2][srcy+2], board[srcx-3][srcy+3]]
            tscore += score_window(window, plyr)
    return tscore

def make_move(inboard, col, player):
    board2 = copy.deepcopy(inboard)
    for i in range(board_rows):
        if board2[0][col] != 0:
            return
        if board2[board_rows - 1 - i][col] not in [1, 2]:
            board2[board_rows - 1 - i][col] = player
            return board2, col

def checkBoard(cboard):
    # sideways
    for i in board:
        for x in range(board_width - 3):
            if i[x] == i[x + 1] == i[x + 2] == i[x + 3] and (i[x] in [1, 2]):
                #print("sideways")
                return True

    # upright
    for i in range(board_rows - 3):
        for x in range(board_width):
            if board[i][x] == board[i + 1][x] == board[i + 2][x] == board[i + 3][x] and (board[i][x] in [1, 2]):
                #print("upright")
                return True

    # diagonal down \
    for i in range(board_rows - 3):
        for x in range(board_width - 3):
            if board[i][x] == board[i + 1][x + 1] == board[i + 2][x + 2] == board[i + 3][x + 3] and (
                    board[i][x] in [1, 2]):
                #print("diag down")
                return True

    # diagonal up /
    for i in range(board_rows - 3):
        for x in range(board_width - 3):
            srcx = i+3
            srcy = x
            if board[srcx][srcy] == board[srcx-1][srcy+1] == board[srcx-2][srcy+2] == board[srcx-3][srcy+3] and (board[srcx][srcy] in [1, 2]):
                #print("diag up")
                return True
    return False

def startGame():
    global board_width
    while True:
        board_width = input("Input board width (or leave empty for default).")
        if board_width.isnumeric():
            board_width = int(board_width)
            break
        elif board_width == "":
            board_width = 7
            break
    global board_rows
    while True:
        board_rows = input("Input board height (or leave empty for default).")
        if board_rows.isnumeric():
            board_rows = int(board_rows)
            break
        elif board_rows == "":
            board_rows = 6
            break
    moves = 0
    global board
    board = []
    state = "start"
    global diff
    diff = ""
    global turn
    turn = 1  # 1 == player, 2 = ai
    for i in range(board_rows):
        board.append([])  # 6 rows, 7 columns in each row
        for x in range(board_width):
            board[i].append(0)
    while True:
        gamemode = input("Select difficulty\n").lower()
        if gamemode in ["random", "easy", "medium", "hard", "r", "e", "m", "h"]:
            dict = {"random": "random", "easy": "easy", "medium": "medium", "hard": "hard", "r": "random", "e": "easy",
                    "m": "medium", "h": "hard"}
            diff = dict[gamemode]
            state = "playing"
            break

    while state == "playing":  # play state start
        for i in range(len(board)):
            print(str(board[i]))

        while True:
            turn = 1
            move = input("Make a move. (column num from 1 to " + str(board_width) + ")")
            if move.isnumeric() and len(move) == 1:
                move = int(move) - 1
                if 0 <= move < board_width and board[0][move] == 0:
                    board = make_move(board, move, turn)[0]
                    break
        moves += 1
        turn = 2
        if checkBoard(board):
            state = "win"
            break
        elif board[0].count(0) == 0:
            print("darw")
            state = "draw"
            break
        else:
            aaa = make_move(board, agent()[0], turn)
            board = aaa[0]
            turn = 1
            if checkBoard(board):
                state = "lose"
                break

    for i in range(len(board)):
        print(str(board[i]))
    if state == "win":
        print(f"Congratulations! You won in {moves} moves against the {diff} bot! ...")

    if state == "lose":
        print(f"Nice try! You lost against the {diff} bot.")

    if state == "draw":
        print(f"Nice try! You drew against the {diff} bot.")

while True:
    startGame()
    while True:
        option = input("Want to try again? (Y/N)")
        if option.lower() in ["y", "yes"]:
            break
        elif option.lower() in ["n", "no"]:
            print("Thanks for playing!")
            break
    if option.lower() in ["n", "yes"]:
        break
