## Game AI (Teeko)
## 12/01/2021
## 2 TODOs

import random
import copy
import numpy as np

## win conditions: 4 in a row horizontally, vertically, or diagonally, or at the corners of a 3x3 square

class Teeko2Player:
    """ An object representation for an AI game player for the game Teeko2.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a Teeko2Player object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    ## returns a list of all possible successors from @state
    def succ(self, state):
        p = self.my_piece
        ps = []
        succs = []
        for row in range(5):
            for col in range(5):
                if state[row][col] == p:
                    ps.append((row,col))
        ## drop phase: add new piece anywhere that is empty
        if len(ps) < 4:
            for row in range(5):
                for col in range(5):
                    if state[row][col] == ' ':
                        b = copy.deepcopy(state)
                        b[row][col] = p
                        succs.append((b, (row, col)))
            return succs
        ## not drop phase: move one piece to adjacent empty space
        for i in range(len(ps)):
            row = ps[i][0]
            col = ps[i][1]
            for c in range(-1, 2):
                for d in range(-1, 2):
                    if -1 < row+c < 5 and -1 < col+d < 5 and not (c == 0 and d == 0):
                        if state[row+c][col+d] == ' ':
                            b = copy.deepcopy(state)
                            b[row][col] = ' '
                            b[row+c][col+d] = p
                            succs.append((b, (row+c, col+d), (row, col)))
        return succs

    ## TODO: improve heuristic function
    def heuristic_game_value(self, state):
        if self.game_value(state) != 0:
            return self.game_value(state)
        me = self.my_piece
        opp = self.opp
        
        m = []
        o = []
        for row in range(5):
            for col in range(5):
                if state[row][col] == me:
                    m.append((row, col))
                if state[row][col] == opp:
                    o.append((row, col))

        if len(m) < 4 or len(o) < 4:
            m_score = 0
            o_score = 0
            for i in range(len(m)):
                if m[i][0] == 2 and m[i][1] == 2:
                    m_score += 0.5
                elif (m[i][0] >= 1 and m[i][0] <= 3) and (m[i][1] >= 1 and m[i][1] <= 3):
                    m_score += 0.16
            for i in range(len(o)):
                if o[i][0] == 2 and o[i][1] == 2:
                    o_score += 0.5
                elif (o[i][0] >= 1 or o[i][0] <= 3) and (o[i][1] >= 1 or o[i][1] <= 3):
                    o_score += 0.16
            return m_score - o_score
        
        hor = abs(m[1][0] - m[0][0]) + abs(m[2][0] - m[0][0]) + abs(m[3][0] - m[0][0]) + abs(m[1][1] - m[0][1] - 1) + abs(m[2][1] - m[0][1] - 2) + abs(m[3][1] - m[0][1] - 3) 
        ver = abs(m[1][0] - m[0][0] - 1) + abs(m[2][0] - m[0][0] - 2) + abs(m[3][0] - m[0][0] - 3) + abs(m[1][1] - m[0][1]) + abs(m[2][1] - m[0][1]) + abs(m[3][1] - m[0][1])
        diag1 = abs(m[1][0] - m[0][0] + 1) + abs(m[2][0] - m[0][0] + 2) + abs(m[3][0] - m[0][0] + 3) + abs(m[1][1] - m[0][1] - 1) + abs(m[2][1] - m[0][1] - 2) + abs(m[3][1] - m[0][1] - 3)
        diag2  = abs(m[1][0] - m[0][0] - 1) + abs(m[2][0] - m[0][0] - 2) + abs(m[3][0] - m[0][0] - 3) + abs(m[1][1] - m[0][1] - 1) + abs(m[2][1] - m[0][1] - 2) + abs(m[3][1] - m[0][1] - 3)
        box = abs(m[1][0] - m[0][0]) + abs(m[2][0] - m[0][0] - 2) + abs(m[3][0] - m[0][0] - 2) + abs(m[1][1] - m[0][1] - 2) + abs(m[2][1] - m[0][1]) + abs(m[3][1] - m[0][1] - 2)
        m_min = min(hor,ver, diag1, diag2, box)

        ohor = abs(o[1][0] - o[0][0]) + abs(o[2][0] - o[0][0]) + abs(o[3][0] - o[0][0]) + abs(o[1][1] - o[0][1] - 1) + abs(o[2][1] - o[0][1] - 2) + abs(o[3][1] - o[0][1] - 3) 
        over = abs(o[1][0] - o[0][0] - 1) + abs(o[2][0] - o[0][0] - 2) + abs(o[3][0] - o[0][0] - 3) + abs(o[1][1] - o[0][1]) + abs(o[2][1] - o[0][1]) + abs(o[3][1] - o[0][1])
        odiag1 = abs(o[1][0] - o[0][0] + 1) + abs(o[2][0] - o[0][0] + 2) + abs(o[3][0] - o[0][0] + 3) + abs(o[1][1] - o[0][1] - 1) + abs(o[2][1] - o[0][1] - 2) + abs(o[3][1] - o[0][1] - 3)
        odiag2  = abs(o[1][0] - o[0][0] - 1) + abs(o[2][0] - o[0][0] - 2) + abs(o[3][0] - o[0][0] - 3) + abs(o[1][1] - o[0][1] - 1) + abs(o[2][1] - o[0][1] - 2) + abs(o[3][1] - o[0][1] - 3)
        obox = abs(o[1][0] - o[0][0]) + abs(o[2][0] - o[0][0] - 2) + abs(o[3][0] - o[0][0] - 2) + abs(o[1][1] - o[0][1] - 2) + abs(o[2][1] - o[0][1]) + abs(o[3][1] - o[0][1] - 2)
        o_min = min(ohor,over, odiag1, odiag2, obox)
        return ( ((24 - m_min) / 24) - ((24 - o_min) / 24) )
            
    ## minimax with heuristic
    ## TODO: implement alpha-beta pruning
    def max_value(self, state, ai_turn, depth):
        if self.game_value(state) != 0:
            return self.game_value(state)
        if depth > 2: ## depth > 2: takes about 4.5 secs, depth > 3: takes about 14 secs
            return self.heuristic_game_value(state)
        succs = self.succ(state)
        s = []
        if ai_turn:
            for i in range(len(succs)):
                s.append(self.max_value(succs[i][0], False, depth+1))
            return max(s)
        else:
            for i in range(len(succs)):
                s.append(self.max_value(succs[i][0], True, depth+1))
            return min(s)

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this Teeko2Player object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
        p = 0
        for i in range(5):
            for j in range(5):
                if self.board[i][j] != ' ':
                    p += 1
        if p < 8:
            drop_phase = True
        else:
            drop_phase = False

        if not drop_phase:
            succs = self.succ(self.board)
            s = []
            for i in range(len(succs)):
                s.append(self.max_value(succs[i][0], False, 0))
            index = np.argmax(s)
            move = []
            move.append(succs[index][1])
            move.append(succs[index][2])
            return move

        move = []
        succs = self.succ(self.board)
        s = []
        for i in range(len(succs)):
            s.append(self.max_value(succs[i][0], False, 0))
        index = np.argmax(s)
        (row, col) = succs[index][1]

        # ensure the destination (row,col) tuple is at the beginning of the move list
        move.insert(0, (row, col))
        return move

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain only the first tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece
        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain only the first tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.

        Returns:
            int: 1 if this Teeko2Player wins, -1 if the opponent wins, 0 if no winner
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # check \ diagonal wins
        for row in range(2):
            for col in range(2):
                if state[row][col] != ' ' and  state[row][col] == state[row+1][col+1] ==  state[row+2][col+2] == state[row+3][col+3]:
                    return 1 if state[row][col] == self.my_piece else -1
        # check / diagonal wins
        for row in range(2):
            for col in range(3, 5):
                if state[row][col] != ' ' and  state[row][col] == state[row+1][col-1] ==  state[row+2][col-2] == state[row+3][col-3]:
                    return 1 if state[row][col] == self.my_piece else -1
        # check 3x3 square corners wins
        for row in range(3):
            for col in range(3):
                if state[row][col] != ' ' and  state[row][col] == state[row+2][col] ==  state[row+2][col+2] == state[row][col+2]:
                    return 1 if state[row][col] == self.my_piece else -1

        return 0 # no winner yet

## gameplay simulation
def main():
    print('Hello, this is Sam')
    ai = Teeko2Player()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
