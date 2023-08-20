
# Name: Hansol Lee
# GitHub: hc-lee
# Date: 5/31/23
# Description: Implement a text-based Othello game.


class Othello:

    def __init__(self):
        """
        Instantiate Othello object.
        Takes no params.
        Initializes board to default center diagonals and an empty player list.
        """
        self._board = [['*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                       ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', 'O', 'X', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', 'X', 'O', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
                       ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*']]
        self._players = []
        self._game_state = True
        self._directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1),
                            (1, -1), (1, 0), (1, 1)]

    def print_board(self):
        """
        Prints the current state of the board.
        Takes no params.
        Returns nothing.
        """
        for row in self._board:
            for column in row:
                print(column, end="  ")
            print()

    def create_player(self, name, color):
        """
        Create and add a new Player object to the list of players.
        Takes name and color as params.
        Returns nothing.
        """
        player_color = color
        self._players.append(Player(name, player_color.lower()))

    def count_pieces(self):
        x = 0
        o = 0
        for row in self._board:
            for column in row:
                if column == 'X':
                    x += 1
                if column == 'O':
                    o += 1
        return [x, o]

    def return_winner(self):
        """
        Iterate over the entire board and count the number of pieces for each color.
        Takes no params.
        Return player with higher count as winner or tie if x == o.
        """
        pieces = self.count_pieces()
        x = pieces[0]
        o = pieces[1]

        if x > o:
            color = 'black'
        elif o > x:
            color = 'white'
        else:
            return "It's a tie"

        for player in self._players:
            if player.get_player_color() == color:
                return f'Winner is {color} player: {player.get_player_name()}'

    def return_available_positions(self, color):
        """
        Iterates over board and adds available positions as coordinates to a list. Used internally
        for play_game().

        Takes color as param.
        Returns list of lists (or tuples) containing coordinate pairs for each valid move for color.
        """
        color_index = {'black': 'X',
                       'white': 'O'}
        positions = []

        for row in range(0, len(self._board)):
            for column, c_elem in enumerate(self._board[row]):
                if c_elem == '.' and self.is_valid_move(row, column, color_index[color], False):
                    pos = (row, column)
                    positions.append(pos)

        return positions

    def is_valid_move(self, row, col, color, flip):
        for direction in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1),
                          (1, -1), (1, 0), (1, 1)]:
            if self.rec_traversal(row, col, direction, color, flip):
                return True

        return False

    def rec_traversal(self, row, col, direction, color, flip):
        row += direction[0]
        col += direction[1]

        if not (0 <= row < len(self._board)) or not (0 <= col < len(self._board[row])):
            return False
        if self._board[row][col] == '*':
            return False
        if self._board[row][col] == '.':
            return False
        if self._board[row][col] == color:
            row -= direction[0]
            col -= direction[1]
            if self._board[row][col] != color and self._board[row][col] != '*' and self._board[row][col] != '.':
                if flip:
                    while self._board[row][col] != color:
                        self._board[row][col] = color  # Flip the piece
                        row -= direction[0]
                        col -= direction[1]
                    return
                else:
                    return True
            return False

        return self.rec_traversal(row, col, direction, color, flip)

    def make_move(self, color, position):
        if position in self.return_available_positions(color):
            if color == 'black':
                self._board[position[0]][position[1]] = 'X'
                for direction in self._directions:
                    self.rec_traversal(position[0], position[1], direction, 'X', True)
            elif color == 'white':
                self._board[position[0]][position[1]] = 'O'
                for direction in self._directions:
                    self.rec_traversal(position[0], position[1], direction, 'O', True)
        return self._board

    def play_game(self, color, position):
        positions = self.return_available_positions(color)
        if position in positions:
            self.make_move(color, position)
            self._game_state = 1
        elif position not in positions and positions != []:
            print(f'Here are the valid moves:{positions}')
            self._game_state = 1
            return 'Invalid move'
        elif positions == [] and self._game_state == 0:
            pieces = self.count_pieces()
            print(f'Game is ended white piece: {pieces[1]} number black piece: {pieces[0]}')
            return self.return_winner()
        else:
            self._game_state = 0
            return positions


class Player:
    """
    Represents a Player with a name and color of piece.
    White = 'O'
    Black = 'X'
    """

    def __init__(self, name, color):
        """
        Instantiates Player object with private fields name and color.
        """
        self._name = name
        self._color = color

    def get_player_name(self):
        """
        Returns name of player
        """
        return self._name

    def get_player_color(self):
        """
        Returns color of player
        """
        return self._color


if __name__ == "__main__":
    game = Othello()
    game.create_player("VERSTUYFT", "white")
    game.create_player("HASSAN", "black")
    game.play_game("black", (3, 4))
    game.play_game("white", (3, 5))
    game.play_game("black", (4, 6))
    game.play_game("white", (3, 7))
    game.play_game("black", (3, 6))
    game.play_game("white", (5, 3))
    game.play_game("black", (3, 8))
    game.make_move("white", (2, 6))
    game.play_game("black", (4, 3))
    game.play_game("white", (3, 3))
    game.play_game("black", (2, 5))
    game.play_game("white", (1, 5))
    game.play_game("black", (3, 2))
    game.play_game("white", (4, 8))
    game.play_game("black", (5, 8))
    game.play_game("white", (3, 1))
    game.play_game("black", (8, 8))
    game.play_game("white", (7, 7))
    game.print_board()
