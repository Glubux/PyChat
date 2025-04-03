import socket
import threading

clients = []  # Liste aller verbundenen Clients mit Namen
server_running = True  # Kontrolliert, ob der Server läuft

def broadcast(message, sender_socket=None):
    """Sendet eine Nachricht an alle Clients außer dem Sender."""
    for client in clients:
        if sender_socket is None or client["socket"] != sender_socket:
            try:
                client["socket"].send(message.encode())
            except:
                clients.remove(client)

def handle_client(client_socket):
    """Empfängt Nachrichten von einem Client und sendet sie an alle anderen."""
    global server_running
    try:
        # Name des Clients empfangen
        name = client_socket.recv(1024).decode().strip()
        if not name:
            client_socket.close()
            return
        if name in clients["name"]:
            print("in liste")
            
        clients.append({"socket": client_socket, "name": name})
        print(f"{name} hat sich verbunden.")
        broadcast(f"{name} hat den Chat betreten.", client_socket)

        while server_running:
            received_data = client_socket.recv(1024).decode()
            if not received_data or received_data.lower() == "exit":
                break

            # Nachricht formatieren und senden
            if "|" in received_data:
                _, message = received_data.split("|", 1)
            else:
                message = received_data  # Falls Format fehlerhaft ist

            broadcast(f"{name}: {message}", client_socket)
            print(f"{name}: {message}")

    except:
        pass

    print(f"{name} hat den Chat verlassen.")
    clients[:] = [c for c in clients if c["socket"] != client_socket]
    broadcast(f"{name} hat den Chat verlassen.", client_socket)
    client_socket.close()

def server_commands():
    """Ermöglicht dem Server-Administrator, Befehle einzugeben."""
    global server_running
    while server_running:
        command = input("> ").strip()

        if command.startswith("message "):
            _, message = command.split(" ", 1)
            broadcast(f"Server: {message}")
            print(f"Server: {message}")

        elif command.startswith("exit "):
            _, username = command.split(" ", 1)
            for client in clients:
                if client["name"] == username:
                    print(f"Verbindung zu {username} wird getrennt...")
                    client["socket"].close()
                    clients.remove(client)
                    broadcast(f"{username} wurde vom Server getrennt.")
                    break
            else:
                print(f"Benutzer {username} nicht gefunden.")

        elif command == "shutdown":
            print("Server wird heruntergefahren...")
            server_running = False
            for client in clients:
                client["socket"].close()
            clients.clear()
            break

        else:
            print("Unbekannter Befehl. Verfügbare Befehle: message <msg>, exit <name>, shutdown")

def start_server():
    """Startet den Server und akzeptiert neue Verbindungen."""
    global server_running
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("46.234.39.165", 12345))
    server.listen()

    print("Server läuft...")
    threading.Thread(target=server_commands, daemon=True).start()  # Server-Commands starten

    while server_running:
        try:
            client_socket, addr = server.accept()
            print(f"Neue Verbindung von {addr}")
            threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()
        except:
            break

    print("Server wurde gestoppt.")
    server.close()

if __name__ == "__main__":
    start_server()