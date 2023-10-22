import getpass
import hashlib
import os
import re
import random
import string
import subprocess

users = {}
users_file = "users.txt"
locked_accounts_file = "locked_accounts.txt"
locked_accounts = set()

def clear_screen():
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)

def load_users():
    global locked_accounts
    if os.path.exists(users_file):
        with open(users_file, "r") as f:
            for line in f:
                try:
                    username, password_hash, security_question, answer = line.strip().split("|")
                    users[username] = {
                        "password": password_hash,
                        "security_question": security_question,
                        "answer": answer
                    }
                except ValueError as e:
                    print(f"Error reading user data from file: {e}")
    if os.path.exists(locked_accounts_file):
        with open(locked_accounts_file, "r") as f:
            locked_accounts = set(f.read().splitlines())

def save_users():
    with open(users_file, "w") as f:
        for username, data in users.items():
            f.write(f"{username}|{data['password']}|{data['security_question']}|{data['answer']}\n")
    with open(locked_accounts_file, "w") as f:
        for username in locked_accounts:
            f.write(f"{username}\n")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password_strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if any(char.islower() for char in password):
        score += 1
    if any(char.isupper() for char in password):
        score += 1
    if any(char.isdigit() for char in password):
        score += 1
    if any(char in string.punctuation for char in password):
        score += 1
    return score

def validate_username(username):
    return re.match(r"^[a-zA-Z0-9_]{3,}$", username) is not None

def sign_up():
    while True:
        username = input("Enter username for sign-up: ")
        if not validate_username(username):
            print("Invalid username. It must be at least 3 characters long and contain only letters, numbers, and underscores.")
            continue
        if username in users:
            print("Username already exists. Please login.")
            login()
            return
        break
    while True:
        password = getpass.getpass("Enter password for sign-up: ")
        score = check_password_strength(password)
        if score < 3:
            print("Weak password! Try using a mix of uppercase letters, lowercase letters, numbers, and special characters.")
            continue
        if score == 3:
            print("Good password.")
        if score == 4:
            print("Strong password!")
        break
    security_question = input("Enter a security question for account recovery: ")
    answer = getpass.getpass("Enter the answer to your security question: ")
    users[username] = {
        "password": hash_password(password),
        "security_question": security_question,
        "answer": answer
    }
    save_users()
    print("Sign-up successful")
    clear_screen()

def reset_password():
    username = input("Enter your username: ")
    if username in users:
        security_question = users[username]["security_question"]
        answer = getpass.getpass(f"Answer the security question: {security_question}: ")
        if users[username]["answer"] == answer:
            new_password = getpass.getpass("Enter new password: ")
            users[username]["password"] = hash_password(new_password)
            save_users()
            print("Password reset successfully.")
            return True
        print("Incorrect answer.")
    else:
        print("Invalid username.")
    return False

def login():
    while True:
        username = input("Enter username for login: ")
        if username in locked_accounts:
            print("Account is locked. Please contact support.")
            return False
        if username not in users:
            print("Invalid username. Please try again.")
            continue
        break
    for _ in range(3):
        password = getpass.getpass("Enter password for login: ")
        if users[username]["password"] == hash_password(password):
            print("Login successful!")
            clear_screen()
            return True
        print("Invalid password. Please try again.")
    locked_accounts.add(username)
    save_users()
    print("Account locked due to too many failed login attempts. Please contact support.")
    return False

def feature_one():
    print("Welcome to the simple calculator!")
    while True:
        operation = input("Enter operation (+, -, *, /) or 'exit' to go back to the menu: ")
        if operation == 'exit':
            break
        if operation not in ['+', '-', '*', '/']:
            print("Invalid operation. Please enter +, -, *, or /.")
            continue
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        if operation == '+':
            print(f"The result is: {num1 + num2}")
        elif operation == '-':
            print(f"The result is: {num1 - num2}")
        elif operation == '*':
            print(f"The result is: {num1 * num2}")
        elif operation == '/':
            if num2 == 0:
                print("Cannot divide by zero.")
                continue
            print(f"The result is: {num1 / num2}")

def feature_two():
    print("Welcome to the number guessing game!")
    while True:
        try:
            lower_bound = int(input("Enter the lower bound: "))
            upper_bound = int(input("Enter the upper bound: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        break
    secret_number = random.randint(lower_bound, upper_bound)
    print(f"Guess the number between {lower_bound} and {upper_bound}.")
    while True:
        try:
            guess = int(input("Enter your guess: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        if guess == secret_number:
            print("Congratulations! You guessed the secret number.")
            break
        elif guess < secret_number:
            print("Too low. Try again.")
        else:
            print("Too high. Try again.")

def interactive_menu():
    print("Welcome to the interactive menu!")
    print("1. Simple Calculator")
    print("2. Number Guessing Game")
    print("3. Exit")
    while True:
        choice = input("Choose an option: ")
        if choice == '1':
            feature_one()
        elif choice == '2':
            feature_two()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def main():
    load_users()
    while True:
        choice = input("Do you have an account? (yes/no/forgot password/exit): ").lower()
        if choice == 'yes':
            if login():
                interactive_menu()
                print("Thank you for using my first tool! Follow me on Instagram @_.rafahl.klr._ for more information.")
                break
        elif choice == 'no':
            sign_up()
        elif choice == 'forgot password':
            if reset_password():
                login()
        elif choice == 'exit':
            break
        else:
            print("Invalid choice. Please enter yes, no, forgot password, or exit.")
        print("\n")

if __name__ == "__main__":
    main()
