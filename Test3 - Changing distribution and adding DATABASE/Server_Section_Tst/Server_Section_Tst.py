import socket
import threading
import sqlite3
from datetime import datetime

connection = sqlite3.connect('players.db', check_same_thread=False)
c = connection.cursor()
# c.execute("SELECT * FROM players")
# rows = c.fetchall()

# for row in rows:
#     print(row)

c.execute("""CREATE TABLE IF NOT EXISTS players (
        name TEXT,
        password TEXT,
        acc_created TEXT,
        max_score REAL
    )""")



host = "127.0.0.1"
port = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(10)

print(f"[INFO] Server listening on {host}:{port}")

clients = {}  # Key: name -- Value: socket


def login(data3, client_socket):
    connection = sqlite3.connect('players.db', check_same_thread=False)
    c = connection.cursor()
    message = data3
    message = message[8:]
    name, password = message.strip().split(", ")

    c.execute("SELECT * FROM players WHERE name = ?", (name,))
    user = c.fetchone()

    if not user:
        # Username not found
        client_socket.send("-1".encode('utf-8'))
        return

    if user[1] != password:
        # Password is incorrect
        client_socket.send("-2".encode('utf-8'))
        return


    clients[name] = client_socket
    response = f"{name}, {user[1]}, {user[2]}, {user[3]}"
    print(response)
    client_socket.send(response.encode('utf-8'))  # Login

def register(data3, client_socket):
    connection = sqlite3.connect('players.db', check_same_thread=False)
    c = connection.cursor()
    message = data3
    message = message[11:]  # Extract the part after '%%%REGISTER'
    name, password = message.split(", ")

    # Check if username already exists by checking the 'name' field
    c.execute("SELECT * FROM players WHERE name = ?", (name,))
    user_exists = c.fetchone()

    if user_exists:
        # Username found
        client_socket.send("-1".encode('utf-8'))  # Username already exists
    else:
        now = datetime.now()
        clients[name] = client_socket
        # Insert the new user into the database (name, password, acc_created, max_score)
        c.execute("INSERT INTO players VALUES (?, ?, ?, ?)", 
                  (name, password, now.strftime("%m/%d/%Y, %H:%M:%S"), 0.0))
        connection.commit()
        client_socket.send("1".encode('utf-8'))  # Registration 

def send_message(data3, client_socket):
    message = data3
    try:
        sender, receiver, text = message.split(", ", 2)
    except:
        return
    print(f"{sender} sent $${text}$$ to {receiver}")

    if receiver in clients:
        clients[receiver].send(f"{sender}: {text}".encode("utf-8"))
    else:
        clients[sender].send(f"{sender}: Receiver {receiver} not connected.".encode("utf-8")) # Send Messages

def update_record(data3, client_socket):
    connection = sqlite3.connect('players.db', check_same_thread=False)
    c = connection.cursor()

    message = data3
    message = message[9:]  # Extract the part after '%%%NEW_REC'
    new_rec, name = message.split(", ")
    print(new_rec)
    print(name)

    c.execute("SELECT max_score FROM players WHERE name = ?", (name,))
    user_exists = c.fetchone()

    if user_exists:
        print ("NEW RECORD!!")
        c.execute("UPDATE players SET max_score = ? WHERE name = ?", (new_rec, name)) # Update Record
        connection.commit() # Update Record
        
def delete_account(data3, client_socket):
    connection = sqlite3.connect('players.db', check_same_thread=False)
    c = connection.cursor()

    message = data3
    message = message[12:]  # Extract the part after '%%%NEW_REC'
    name = message

    c.execute("SELECT * FROM players WHERE name = ?", (name,))
    user_exists = c.fetchone()

    if user_exists:
        c.execute("DELETE FROM players WHERE name = ?", (name,))
        connection.commit()  # Save changes
        print(f"[INFO] Player {name} deleted from database.") # Delete Account

def handle_client2(client_socket):
    try:
        while True:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                if message.startswith("%%%LOGIN"):
                    login(message, client_socket)
                    continue
                elif message.startswith("%%%REGISTER"):
                    register(message, client_socket)
                    continue
                elif message.startswith("%%%NEWREC"):
                    update_record(message, client_socket)
                elif message.startswith("%%%DELETEACC"):
                    delete_account(message, client_socket)
                else:
                    send_message(message, client_socket)
            else:
                break
    except ConnectionResetError:
        print(f"[INFO] Client disconnected abruptly.")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
    finally:
        for name, socket in list(clients.items()):
            if socket == client_socket:
                del clients[name]
                break
        client_socket.close() # Handle Client

while True:
    connection.close()
    client_socket, addr = server.accept()
    threading.Thread(target=handle_client2, args=(client_socket,), daemon=True).start()
