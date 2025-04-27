import socket
import threading

ALLOWED_IPS = None  # []
REQUIRE_PASSWORD = True
SERVER_PASSWORD = "meinpasswort123"

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.server_running = True

    def broadcast(self, message, sender_socket=None):
        for client in self.clients:
            if sender_socket is None or client["socket"] != sender_socket:
                try:
                    client["socket"].send(message.encode())
                except Exception as e:
                    print(f"Fehler beim Senden an {client['name']}: {e}")
                    self.remove_client(client["socket"])

    def remove_client(self, client_socket):
        for client in self.clients:
            if client["socket"] == client_socket:
                print(f"Verbindung zu {client['name']} ({client['ip']}) getrennt.")
                self.clients.remove(client)
                client_socket.close()
                break

    def handle_client(self, client_socket, addr):
        name = "<Unbekannt>"
        try:
            if ALLOWED_IPS and addr[0] not in ALLOWED_IPS:
                print(f"Verbindung von {addr[0]} blockiert.")
                client_socket.close()
                return

            name_bytes = client_socket.recv(1024)
            name = name_bytes.decode('utf-8', errors='replace').strip()

            if any(client["name"] == name for client in self.clients):
                client_socket.send("Name bereits vergeben, bitte wähle einen anderen.".encode())
                client_socket.close()
                return

            if REQUIRE_PASSWORD:
                password_bytes = client_socket.recv(1024)
                password = password_bytes.decode('utf-8', errors='replace').strip()
                if password != SERVER_PASSWORD:
                    client_socket.send("Falsches Passwort.".encode())
                    client_socket.close()
                    return

            self.clients.append({"socket": client_socket, "name": name, "ip": addr[0]})
            print(f"{name} ({addr[0]}) hat sich verbunden.")
            self.broadcast(f"{name} hat den Chat betreten.", client_socket)

            while self.server_running:
                data = client_socket.recv(1024)
                if not data:
                    break

                message = data.decode('utf-8', errors='replace').strip()
                if message.lower() == "exit":
                    break

                self.broadcast(f"{name}: {message}", client_socket)
                print(f"{name} ({addr[0]}): {message}")

        except Exception as e:
            print(f"Fehler beim Verarbeiten von {name} ({addr[0]}): {e}")

        finally:
            print(f"{name} ({addr[0]}) hat den Chat verlassen.")
            self.remove_client(client_socket)
            self.broadcast(f"{name} hat den Chat verlassen.", client_socket)

    def server_commands(self):
        while self.server_running:
            command = input("> ").strip()

            if command.startswith("message "):
                _, message = command.split(" ", 1)
                self.broadcast(f"Server: {message}")
                print(f"Server: {message}")

            elif command.startswith("exit "):
                _, username = command.split(" ", 1)
                for client in self.clients:
                    if client["name"] == username:
                        self.remove_client(client["socket"])
                        self.broadcast(f"{username} wurde vom Server getrennt§.")
                        break
                else:
                    print(f"Benutzer {username} nicht gefunden.")

            elif command == "shutdown":
                print("Server wird heruntergefahren...")
                self.server_running = False
                for client in self.clients:
                    self.remove_client(client["socket"])
                break

            else:
                print("Unbekannter Befehl. Verfügbare Befehle: message <msg>, exit <name>, shutdown")

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen()

        print("Server läuft...")
        threading.Thread(target=self.server_commands, daemon=True).start()

        while self.server_running:
            try:
                client_socket, addr = server.accept()
                print(f"Neue Verbindung von {addr}")
                threading.Thread(target=self.handle_client, args=(client_socket, addr), daemon=True).start()
            except Exception as e:
                print(f"Fehler beim Akzeptieren der Verbindung: {e}")
                break

        print("Server wurde gestoppt.")
        server.close()

if __name__ == "__main__":
    host = "46.234.39.165"
    port = 12345
    chat_server = ChatServer(host, port)
    chat_server.start_server()
