import socket
import threading
import time


class TicTacToeServer:
    def __init__(self, host="127.0.0.1", port=12345):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(2)
        print(f"Server started on {host}:{port}")
        self.players = []
        self.player_symbols = ["X", "O"]
        self.winner_streak = {"X": 0, "O": 0}
        self.start_time = None

    def accept_players(self):
        print("Waiting for players to join...")
        while len(self.players) < 2:
            conn, addr = self.server.accept()
            self.players.append((conn, addr))
            print(f"Player {self.player_symbols[len(self.players) - 1]} connected from {addr}.")
            conn.sendall(f"Welcome! You are Player {self.player_symbols[len(self.players) - 1]}.\n".encode())
            if len(self.players) == 2:
                threading.Thread(target=self.run_game).start()

    def broadcast(self, message, exclude=None):
        """Send a message to all players except the excluded one."""
        for conn, _ in self.players:
            if conn != exclude:
                try:
                    conn.sendall(message.encode())
                except:
                    pass

    def run_game(self):
        """Main game loop."""
        self.start_time = time.time()
        board = [[" " for _ in range(3)] for _ in range(3)]
        current_turn = 0

        while True:
            conn, _ = self.players[current_turn]
            try:
                self.broadcast(self.format_board(board))
                conn.sendall(f"Your move ({self.player_symbols[current_turn]}): ".encode())
                move = conn.recv(1024).decode().strip()

                if not move or move.lower() == "quit":
                    raise ConnectionResetError(f"Player {self.player_symbols[current_turn]} quit the game.")
                if self.is_valid_move(move, board):
                    self.make_move(move, board, self.player_symbols[current_turn])
                    if self.check_winner(board, self.player_symbols[current_turn]):
                        self.broadcast(self.format_board(board))
                        self.broadcast(f"Player {self.player_symbols[current_turn]} wins!\n")
                        self.winner_streak[self.player_symbols[current_turn]] += 1
                        break
                    if self.is_draw(board):
                        self.broadcast(self.format_board(board))
                        self.broadcast("It's a draw!\n")
                        break
                    current_turn = 1 - current_turn
                else:
                    conn.sendall("Invalid move. Try again.\n".encode())
            except ConnectionResetError as e:
                print(e)
                self.handle_disconnection(current_turn)
                break
        self.end_game()

    def handle_disconnection(self, current_turn):
        """Handle when a player disconnects."""
        conn, _ = self.players[current_turn]
        self.broadcast(f"Player {self.player_symbols[current_turn]} has disconnected. Game over.\n", exclude=conn)
        conn.close()
        self.players.remove((conn, _))

    def end_game(self):
        """End the game and display stats."""
        duration = time.time() - self.start_time
        self.broadcast(f"Game duration: {duration:.2f} seconds.\n")
        self.broadcast(
            f"Streaks: Player X - {self.winner_streak['X']}, Player O - {self.winner_streak['O']}.\n"
        )
        for conn, _ in self.players:
            conn.sendall("Game over. Thanks for playing!\n".encode())
            conn.close()
        self.server.close()

    @staticmethod
    def format_board(board):
        rows = ["  1   2   3"]
        for idx, row in enumerate(board):
            rows.append(f"{chr(65 + idx)} " + " | ".join(row))
            if idx < 2:
                rows.append("  ---+---+---")
        return "\n".join(rows)

    @staticmethod
    def is_valid_move(move, board):
        if len(move) != 2:
            return False
        row, col = move.upper()
        if row not in "ABC" or col not in "123":
            return False
        row_idx, col_idx = ord(row) - 65, int(col) - 1
        return board[row_idx][col_idx] == " "

    @staticmethod
    def make_move(move, board, symbol):
        row, col = move.upper()
        row_idx, col_idx = ord(row) - 65, int(col) - 1
        board[row_idx][col_idx] = symbol

    @staticmethod
    def check_winner(board, symbol):
        for row in board:
            if all(cell == symbol for cell in row):
                return True
        for col in zip(*board):
            if all(cell == symbol for cell in col):
                return True
        if all(board[i][i] == symbol for i in range(3)) or all(
            board[i][2 - i] == symbol for i in range(3)
        ):
            return True
        return False

    @staticmethod
    def is_draw(board):
        return all(cell != " " for row in board for cell in row)


if __name__ == "__main__":
    TicTacToeServer().accept_players()
