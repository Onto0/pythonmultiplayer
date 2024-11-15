class Game:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.turn = 'X'

    def display_board(self):
        """Display the current game board."""
        for row in self.board:
            print(' | '.join(row))
            print('---------')

    def make_move(self, move):
        """Process the player's move."""
        row, col = self.get_coordinates(move)
        if self.board[row][col] == ' ':
            self.board[row][col] = self.turn
            return True
        return False

    def get_coordinates(self, move):
        """Convert the move string (e.g., 'A1') to board coordinates (row, col)."""
        mapping = {'a': 0, 'b': 1, 'c': 2}
        row = mapping[move[0].lower()]
        col = int(move[1]) - 1
        return row, col

    def toggle_turn(self):
        """Switch turns between X and O."""
        self.turn = 'O' if self.turn == 'X' else 'X'

    def check_winner(self):
        """Check for a winner."""
        for row in self.board:
            if row[0] == row[1] == row[2] != ' ':
                return row[0]
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                return self.board[0][col]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]
        return None

    def is_board_full(self):
        """Check if the board is full."""
        for row in self.board:
            if ' ' in row:
                return False
        return True
