import socket
import threading
import sqlite3
from datetime import datetime
from mistralai import Mistral
import json

# AI BOT Configuration
API_KEY = "dJajB61WhVXvUvjTGisMEkRVrueE1w8v"
client = Mistral(api_key=API_KEY)
MODEL = "mistral-large-latest"

# Database Configuration
DATABASE = 'players.db'

# Server Configuration
HOST = "127.0.0.1"
PORT = 12345

# Initialize the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(10)

print(f"[INFO] Server listening on {HOST}:{PORT}")

# Dictionary to keep track of connected clients
clients = {}  # Key: name -- Value: socket

# Database Helper Functions
def get_db_connection():
    return sqlite3.connect(DATABASE, check_same_thread=False)

def initialize_database():
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS players (
                name TEXT PRIMARY KEY,
                password TEXT,
                acc_created TEXT,
                max_score REAL,
                friend_list TEXT
            )""")
        
        # Check if 'friend_list' column exists, if not, add it
        c.execute("PRAGMA table_info(players)")
        columns = [col[1] for col in c.fetchall()]
        if "friend_list" not in columns:
            c.execute("ALTER TABLE players ADD COLUMN friend_list TEXT")
        conn.commit()

# Initialize the database
initialize_database()



def update_max_score_hacking(username, new_score):
    try:
        with get_db_connection() as conn:
            c = conn.cursor()

            # Update the player's max score
            c.execute("UPDATE players SET max_score = ? WHERE name = ?", (new_score, username))
            conn.commit()  # Save changes

            print(f"Updated {username}'s max_score to {new_score}")

    except Exception as e:
        print(f"Error updating max_score: {e}") # Cheating Scores

def update_account_creation_date(username, new_date):
    try:
        with get_db_connection() as conn:
            c = conn.cursor()

            # Update the account creation date
            c.execute("UPDATE players SET acc_created = ? WHERE name = ?", (new_date, username))
            conn.commit()  # Save changes

            print(f"Updated {username}'s account creation date to {new_date}")

    except Exception as e:
        print(f"Error updating account creation date: {e}") # Cheating Dates

# update_max_score_hacking("EXVLO", 1980000)
# update_max_score_hacking("ELENE", 8190000)
# update_max_score_hacking("NIKO", 176123)
# update_max_score_hacking("GUGA", 50000)
# update_max_score_hacking("123", 1230000)

# update_account_creation_date("EXVLO", "09/08/2021 12:00:00")
# update_account_creation_date("ELENE", "04/19/2022 19:19:19")
# update_account_creation_date("NIKO", "01/14/2025 15:45:23")
# update_account_creation_date("GUGA", "01/01/2023 15:45:23")
# update_account_creation_date("123", "01/02/2023 12:31:23")



# Server Functions
def login(data, client_socket):
    with get_db_connection() as conn:
        c = conn.cursor()
        name, password = data[8:].split(", ")

        c.execute("SELECT * FROM players WHERE name = ?", (name,))
        user = c.fetchone()

        if not user:
            client_socket.send("-1".encode('utf-8'))  # Username not found
            return

        if user[1] != password:
            client_socket.send("-2".encode('utf-8'))  # Incorrect password
            return

        friend_list = json.loads(user[4]) if user[4] else []
        response = {
            "name": user[0],
            "password": user[1],
            "acc_created": user[2],
            "max_score": user[3],
            "friend_list": friend_list  # Now a valid JSON array
        }

        # Send the JSON response to the client
        client_socket.send(json.dumps(response).encode('utf-8'))
        clients[name] = client_socket # Login

def register(data, client_socket):
    with get_db_connection() as conn:
        c = conn.cursor()
        name, password = data[11:].split(", ")

        c.execute("SELECT * FROM players WHERE name = ?", (name,))
        if c.fetchone():
            client_socket.send("-1".encode('utf-8'))  # Username already exists
            return

        now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        c.execute("INSERT INTO players VALUES (?, ?, ?, ?, ?)", (name, password, now, 0.0, ""))
        conn.commit()
        clients[name] = client_socket
        client_socket.send("1".encode('utf-8'))  # Register

def send_message(data, client_socket):
    try:
        sender, receiver, text = data.split(", ", 2)
        print(f"{sender} sent $${text}$$ to {receiver}")

        if receiver in clients:
            clients[receiver].send(f"{sender}: {text}".encode("utf-8"))
        else:
            clients[sender].send(f"{sender}: Receiver {receiver} not connected.".encode("utf-8"))

        if text.startswith("!ASKAI"):
            text = text[6:]
            try:
                chat_response = client.chat.complete(
                    model=MODEL,
                    messages=[{"role": "user", "content": f"Only Short Answers with few Words: {text}"}]
                )
                answer = chat_response.choices[0].message.content.strip()
                ai = "AI"
                clients[receiver].send(f"{ai}: {answer}".encode("utf-8"))
                clients[sender].send(f"{ai}: {answer}".encode("utf-8"))
            except Exception as e:
                print(f"Error Occurred While Chatting With AI: {e}")
    except ValueError:
        print("Invalid message format.") # Send Messages

def update_record(data, client_socket):
    with get_db_connection() as conn:
        c = conn.cursor()
        new_rec, name = data[9:].split(", ")

        c.execute("UPDATE players SET max_score = ? WHERE name = ?", (new_rec, name))
        conn.commit()
        print(f"[INFO] Updated record for {name} to {new_rec}") # Update Record

def delete_account(data, client_socket):
    with get_db_connection() as conn:
        c = conn.cursor()
        name = data[12:]

        c.execute("DELETE FROM players WHERE name = ?", (name,))
        conn.commit()
        print(f"[INFO] Player {name} deleted from database.") # Delete Account

def add_friends(data, client_socket):
    with get_db_connection() as conn:
        c = conn.cursor()
        name, friend = data[12:].split(", ")

        c.execute("SELECT friend_list FROM players WHERE name = ?", (name,))
        existing_friends = c.fetchone()[0]

        if existing_friends:
            try:
                friend_list = json.loads(existing_friends)
            except json.JSONDecodeError:
                friend_list = existing_friends.split(",")  # Fallback in case of legacy data
        else:
            friend_list = []

        if friend not in friend_list:
            friend_list.append(friend)
            c.execute("UPDATE players SET friend_list = ? WHERE name = ?", (json.dumps(friend_list), name))
            conn.commit()
            print(f"[INFO] {friend} added to {name}'s friend list.") # Add Friend

def remove_friends(data, client_socket):
    with get_db_connection() as conn:
        c = conn.cursor()
        name, friend = data[15:].split(", ")

        c.execute("SELECT friend_list FROM players WHERE name = ?", (name,))
        existing_friends = c.fetchone()[0]

        if existing_friends:
            try:
                friend_list = json.loads(existing_friends)
            except json.JSONDecodeError:
                friend_list = existing_friends.split(",")  # Fallback in case of legacy data
        else:
            friend_list = []

        if friend in friend_list:
            friend_list.remove(friend)
            c.execute("UPDATE players SET friend_list = ? WHERE name = ?", (json.dumps(friend_list), name))
            conn.commit()
            print(f"[INFO] {friend} removed from {name}'s friend list.") # Remove Friend

def send_score_data(client_socket):
    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT max_score, acc_created FROM players")
            data = c.fetchall()  # List of tuples like [(50, '2024-01-30 12:34:56'), (30, '2024-01-29 10:20:30')]

            # Extract max_score and acc_created
            max_score_list = [row[0] for row in data]  # First column
            acc_created_list = [row[1] for row in data]  # Second column

            # Send response to client
            response = {
                "%%%max_score_list": max_score_list,
                "%%%acc_created_list": acc_created_list
            }
            client_socket.send(json.dumps(response).encode('utf-8'))

    except Exception as e:
        print(f"Error occurred while retrieving data from players: {e}")

def handle_client(client_socket):
    try:
        while True:
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                break

            if message.startswith("%%%LOGIN"):
                login(message, client_socket)
            elif message.startswith("%%%REGISTER"):
                register(message, client_socket)
            elif message.startswith("%%%NEWREC"):
                update_record(message, client_socket)
            elif message.startswith("%%%DELETEACC"):
                delete_account(message, client_socket)
            elif message.startswith("%%%ADDFRIEND"):
                add_friends(message, client_socket)
            elif message.startswith("%%%REMOVEFRIEND"):
                remove_friends(message, client_socket)
            elif message.startswith("%%%GETSTATS"):
                send_score_data(client_socket)
            else:
                send_message(message, client_socket)
    except ConnectionResetError:
        print("[INFO] Client disconnected abruptly.")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
    finally:
        for name, socket in list(clients.items()):
            if socket == client_socket:
                del clients[name]
                break
        client_socket.close()

# Main server loop
while True:
    client_socket, addr = server.accept()
    threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()