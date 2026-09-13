import random   #für password generator
import string   #um possible characters einfacher darzustellen
import json     #speichern und laden meiner datei wo alles gespeichert wird
from cryptography.fernet import Fernet #zum encrypten/decrypten der passwörter
import os

# Hier wird alles drinnen gespeichert, später dann in einer json
safe = {}

# alle möglichen characters
possible_chars = string.ascii_lowercase + string.ascii_uppercase + string.digits + "!+-.,#?$%*"

#directory für encrypten decrpyten
script_dir = os.path.dirname(os.path.abspath(__file__))
keys_dir = os.path.join(script_dir,"..","KEYS")

#lädt die gespeicherten daten in die session
def load_from_file(filename="passwords.json"):
    global safe
    try:
        with open(os.path.join(script_dir,filename), "r") as f:
            safe = json.load(f)
    except FileNotFoundError:
        safe = {}

#speichert alles auf die json file
def save_to_file(filename="passwords.json"):
    with open(os.path.join(script_dir,filename), "w") as f:
        json.dump(safe, f, indent=4)

#generiert den fernet key zum crypten
def load_or_create_key():
    if not os.path.exists(keys_dir):
        os.makedirs(keys_dir)
    try:
        with open(os.path.join(keys_dir,"password_key.key"), "rb") as f:
            loaded_key = f.read()
        return loaded_key
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open(os.path.join(keys_dir,"password_key.key"), "wb") as f:
            f.write(key)
        return key
    
#encrypten des passworts
def encrypt_password(encrypted_password):
    key = load_or_create_key()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(encrypted_password.encode())
    return encrypted.decode()

#decrypten des passworts
def decrypt_password(encrypted_password):
    key = load_or_create_key()
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_password.encode())
    return decrypted.decode()

# Password generator für reines Password generieren
def password_generator(min_char=8, max_chars=20):
    password = "".join(random.choice(possible_chars) for _ in range(random.randint(min_char, max_chars)))
    return password

#print(password_generator())

#check ob password in valid is
def is_password_valid(password, min_length=8):
    if len(password) < min_length:
        return False
    if not set(password).issubset(set(possible_chars)):
        return False
    return True

#Hinzufügen von einem Password
def create_password(password=None, username=None, service=None):

    while service is None or service_choice == "n":
        service = input("For what service do you want to create an entry? *casesensitive*  ")
        while service == "":
            service = input("Service can't be empty. Please retry:   ")
        print("Your input: ", service)
        service_choice = input("Press Enter to confirm, or type 'n' to re-enter:   ")
        while service_choice.lower() != "" and service_choice.lower() != "n":
            service_choice = input("Please press Enter or type 'n':   ")
        if service_choice == "":
            print("Well done!")
    if service in safe:
        print("You already have data saved for this service.    ")
        choice = input("Do you want to change your password? Press Enter for yes, or type 'n' for no:   ")
        while choice.lower() != "" and choice.lower() != "n":
            choice = input("Please press Enter or type 'n':   ")
        if choice.lower() == "":
            update_password()
            return
        else:
            return

    while password is None:
        password_choice = input("Enter your password or hit Enter for a random one:   ")
        if password_choice == "":
            password_choice = password_generator()
            print("Generated:", password_choice)
            confirm = input("Press Enter to accept it, or type 'n' to redo:   ")
            while confirm.lower() != "" and confirm.lower() != "n":
                confirm = input("Please press Enter or type 'n':   ")
            if confirm.lower() == "":
                password = password_choice
        elif is_password_valid(password_choice):
            password = password_choice
        else:
            print("""
Password Conditions:

- Only upper- and lowercase letters
- 0-9 digits
- !+-.,#?$%* are allowed
- min. 8 characters

            """)

    while username is None or username_choice == "n":
        username = input("Lastly your username/email:   ")
        while username == "":
            username = input("Username/email can't be empty. Please retry:   ")
        print("Your input: ", username)
        username_choice = input("Press Enter to confirm, or type 'n' to re-enter:   ")
        while username_choice.lower() != "" and username_choice.lower() != "n":
            username_choice = input("Please press Enter or type 'n':   ")
        if username_choice == "":
            print("Great, now that's finished too!")

    safe[service] = {"username": username, "password": encrypt_password(password)}
    save_to_file()
    print(f"""
        Service: {service}
        Username: {username}
        Password: {password}

        Succesfully saved!
    """)


# Updaten eines Password/Username
def update_password():
    service = input("For which service do you want to change your login credentials? *casesensitive  ")
    while service == "":
        service = input("You can't enter an empty input:   ")

    while service not in safe:
        print(f"There is no such service as {service}")
        service = input("Please enter an existing service or enter 'quit' to leave the programm:   ")
        if service.lower() == "quit":
            return
    print(f"""
    Service: {service}
    Username: {safe[service]["username"]}
    Password: {decrypt_password(safe[service]["password"])}
    """)

    print("""
What do you want to change?

1 - Username/email
2 - Password
3 - Both
""")
    choice = input("Your choice:   ")

    while choice != "1" and choice != "2" and choice != "3":
        choice = input("Please enter 1, 2 or 3:   ")

    #Username changen
    if choice in ("1", "3"):
        print("Your current username/email: ", safe[service]["username"])
        username = input("What shall your changed login credential be?\n")
        if username == "":
            username = "[no username/email given]"
        safe[service]["username"] = username
        save_to_file()
        print(f"Succesfully changed your username/email to {username}")

    #Password changen
    if choice in ("2", "3"):
        print("Your current password: ", decrypt_password(safe[service]["password"]))
        password_confirmed = False

        while not password_confirmed:
            password_choice = input("Press Enter for a random generated password, or type 'n' to choose your own:   ")
            while password_choice.lower() != "" and password_choice.lower() != "n":
                password_choice = input("Please press Enter or type 'n':   ")

            if password_choice.lower() == "":
                password = password_generator()
                final_password_choice = input(f"New password is {password}. Press Enter to accept, or type 'n' to redo:   ")
                while final_password_choice.lower() != "" and final_password_choice.lower() != "n":
                    final_password_choice = input("Please press Enter or type 'n':   ")

                if final_password_choice.lower() == "":
                    password_confirmed = True
            else:
                while not password_confirmed:
                    password = input("Please enter your desired password:   ")
                    if not is_password_valid(password):
                        print("""
Password Conditions:
- Only upper- and lowercase letters
- 0-9 digits
- !+-.,#?$%* are allowed
- min. 8 characters
                        """)
                    else:
                        password_confirmation = input("Please repeat it to confirm:   ")
                        if password_confirmation != password:
                            print("The passwords don't match")
                        else:
                            password_confirmed = True

        safe[service]["password"] = encrypt_password(password)
        save_to_file()
        print("Great, password confirmed and saved!")

#hier kann man die passwörter anschauen die bisher gespeichert wurden
def view_password():
    choice = input("View a specific service or all your saved data? (s/a)   ")
    while choice.lower() != "s" and choice.lower() != "a":
        choice = input("Please enter either 's' for specific or 'a' for all:   ")
    if choice.lower() == "s":
        service_choice = input("Please enter the service you want the login credentials for:   ")
        while service_choice not in safe:
            service_choice = input("Please enter an already existing service, or create a new one by typing 'new':   ")
            if service_choice.lower() == "new":
                create_password()
                return
        print(f"""
Your saved data:

Service: {service_choice}
Username: {safe[service_choice]["username"]}
Password: {decrypt_password(safe[service_choice]["password"])}

        """)
        return
    else:
        for i in safe:
            print(f"""
---------------------------------------------
Service: {i}
Username: {safe[i]["username"]}
Password: {decrypt_password(safe[i]["password"])}
---------------------------------------------
""")
        return



#entfernen eines Eintrags
def delete_password():
    choice = input("Which service do you want to delete?    ")
    while choice not in safe and choice.lower() != "quit":
        choice = input("Please enter a already existing service or type *quit* to quit the programm:    ") 
    if choice.lower() == "quit":
        print("Deletion cancelled")
        return
    else:
        final_choice = input(f"Sure you want to delete the data for {choice}? *yes* for accepting and *no* for quitting the programm and stopping the process.    ")
        while final_choice.lower() != "yes" and final_choice.lower() != "no":
            final_choice = input("Enter either *yes* for confirmation or *no* to stop:  ")
        if final_choice.lower() == "yes":
            del safe[choice]
            print("Succesfully deleted the data for", choice)
            save_to_file()
            return
        else:
            print("Deletion prevented.")
            return

load_from_file()
load_or_create_key()
delete_password()
view_password()