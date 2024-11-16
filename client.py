import socket


class TicTacToeClient:
    def __init__(self, host, port=12345):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

    def run(self):
        try:
            while True:
                server_message = self.client.recv(1024).decode()
                if not server_message:
                    print("Connection lost. The server may have closed.")
                    break
                elif "Your move" in server_message:
                    print(server_message)
                    move = input("Enter your move (e.g., A1, B2) or 'quit' to leave: ")
                    self.client.sendall(move.encode())
                elif "Play again?" in server_message:
                    print(server_message)
                    response = input("Play again? (yes/no): ").lower()
                    self.client.sendall(response.encode())
                    if response == "no":
                        print("Thanks for playing!")
                        break
                else:
                    print(server_message)
        except ConnectionResetError:
            print("The server closed the connection.")
        finally:
            self.client.close()


if __name__ == "__main__":
    server_ip = input("Enter the server IP address: ")
    client = TicTacToeClient(server_ip)
    client.run()
