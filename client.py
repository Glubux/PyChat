import socket
import threading

data = {
    "name": "name",
    "message": "message"
}

def receive_messages(client_socket):
    """Empfängt Nachrichten vom Server und gibt sie aus."""
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print("\n" + message)
        except:
            break

def start_client():
    data["name"] = input("Wie lautet dein Name: ")

    """Startet den Client und ermöglicht das Senden von Nachrichten."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("46.234.39.165", 12345))  # Deine IP bleibt erhalten

    # Sende den Namen direkt nach der Verbindung
    client.send(data["name"].encode())

    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

    while True:
        data["message"] = input("> ")
        if data["message"].lower() == "exit":
            break
        
        # Sende die Nachricht als "Name|Nachricht"
        client.send(f"{data['name']}|{data['message']}".encode())

    client.close()

if __name__ == "__main__":
    start_client()