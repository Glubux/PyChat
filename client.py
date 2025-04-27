import socket
import threading

class ChatClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = None
        self.username = None
        self.is_connected = False

    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))
            self.is_connected = True
            print(f"✅ Verbunden mit {self.server_ip}:{self.server_port}")

        except Exception as e:
            print(f"❌ Verbindungsfehler: {e}")
            self.is_connected = False

    def send_message(self, message):
        if self.is_connected:
            try:
                self.client_socket.send(message.encode())

            except Exception as e:
                print(f"❌ Fehler beim Senden der Nachricht: {e}")
                self.disconnect_from_server()

    def receive_messages(self):
        while self.is_connected:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8', errors='replace')
                print(f"\n{message}")

            except OSError:
                break

            except Exception as e:
                print(f"❌ Fehler beim Empfangen der Nachricht: {e}")
                break

        self.is_connected = False

    def get_input(self):
        while self.is_connected:
            try:
                user_input = input("> ")
                if user_input.lower() == "exit":
                    self.send_message("exit")
                    self.disconnect_from_server()
                    break
                self.send_message(user_input)

            except (KeyboardInterrupt, EOFError):
                self.disconnect_from_server()
                break

    def set_username_and_password(self):
        self.username = input("Wie lautet dein Name? ").strip()
        while not self.username:
            self.username = input("Bitte gültigen Namen eingeben: ").strip()

        self.send_message(self.username)

        if REQUIRE_PASSWORD:
            password = input("Passwort: ").strip()
            self.send_message(password)

    def disconnect_from_server(self):
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
        self.is_connected = False
        print("Verbindung zum Server wurde beendet.")

    def start(self):
        self.connect_to_server()
        if self.is_connected:
            self.set_username_and_password()
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.start()
            self.get_input()
            receive_thread.join()


SERVER_IP = "46.234.39.165"
SERVER_PORT = 12345
REQUIRE_PASSWORD = True

if __name__ == "__main__":
    client = ChatClient(SERVER_IP, SERVER_PORT)
    client.start()
