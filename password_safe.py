import random   #für password generator
import string   #um possible characters einfacher darzustellen
import json     #speichern und laden meiner datei wo alles gespeichert wird
from cryptography.fernet import Fernet #zum encrypten/decrypten der passwörter
import streamlit as st  #für mein browser UI
import os   #um die paths für das cryptographen, laden, speichern einfacher zu machen

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
def create_password():

    overwrite = False    
    service = st.text_input("Service(casesensitive): ").strip()
    username = st.text_input("Username/Email:").strip()
    password = st.text_input("Password:").strip()
    password_confirm = st.text_input("Confirm password:").strip()
    if st.button("Save:"):
        if service == "":
            st.error("Service can't be empty!")
        elif username == "":
            st.error("Username/Email can't be empty!")
        elif password == "" or password_confirm == "":
            st.error("Password can't be empty!")
        elif not is_password_valid(password):
            st.error("The password isn't valid.")
            st.text("""
Password Conditions:

- Only upper- and lowercase letters
- 0-9 digits
- !+-.,#?$%* are allowed
- min. 8 characters

            """)
        elif password != password_confirm:
            st.error("The passwords don't match!")
        elif service in safe:
            st.warning(f"An entry for '{service}' already exists.")
            overwrite = st.checkbox("Overwrite existing entry?")
        else:
            overwrite = True

        if overwrite == True:
                safe[service] = {"username": username, "password": encrypt_password(password)}
                st.success("Succesfully saved!")


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
def read_password():
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
create_password()