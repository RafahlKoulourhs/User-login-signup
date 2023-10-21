import getpass
import hashlib
import os

users = {}
users_file = "users.txt"

def load_users():
    if os.path.exists(users_file):
        with open(users_file, "r") as f:
            for line in f:
                username, password_hash = line.strip().split(":")
                users[username] = password_hash

def save_users():
    with open(users_file, "w") as f:
        for username, password_hash in users.items():
            f.write(f"{username}:{password_hash}\n")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def sign_up():
    username = input("Enter username for sign-up: ")
    if username in users:
        print("Username already exists")
        return False
    password = getpass.getpass("Enter password for sign-up: ")
    users[username] = hash_password(password)
    save_users()
    print("Sign-up successful")
    return True

def login():
    username = input("Enter username for login: ")
    while True:
        password = getpass.getpass("Enter password for login: ")
        if username in users and users[username] == hash_password(password):
            print("Login successful!")
            print("Thank you for using my first tool! Follow me on Instagram @_.rafahl.klr._ for more information.")
            return True
        else:
            print("Invalid password. Please try again.")

def main():
    load_users()
    while True:
        choice = input("Do you have an account? (yes/no/exit): ")
        if choice.lower() == 'yes' or choice.lower() == 'no':
            if choice.lower() == 'no':
                if sign_up():
                    print("Sign-up successful! Now, please log in with your new account.")
            while not login():
                print("Please try logging in again.")
            break
        elif choice.lower() == 'exit':
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
