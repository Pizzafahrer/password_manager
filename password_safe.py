import random
import string
import json

# Hier wird alles drinnen gespeichert, später dann in einer json
safe = {}

# alle möglichen characters
possible_chars = string.ascii_lowercase + string.ascii_uppercase + string.digits + "!+-.,#?$%*"


def load_from_file(filename="passwords.json"):
    global safe
    try:
        with open(filename, "r") as f:
            safe = json.load(f)
    except FileNotFoundError:
        safe = {}


def save_to_file(filename="passwords.json"):
    with open(filename, "w") as f:
        json.dump(safe, f, indent=4)


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
def add_password(password = None, username = None, service = None):

    while service == None or service_choice == "n":
        service = input("For what service do you want to create a entry?   ")
        while service == "":
            service = input("Service can't be empty. Please retry. ") 
        print("Your input: ", service)
        service_choice = input("Confident you typed it correctly, if yes then hit enter otherwise type n.")
        while service_choice.lower() != "" and service_choice.lower() != "n":
             service_choice = input("Please hit either enter or type n  ")
        if service_choice == "":
             print("Superb performance!")
    if service in safe: 
        print("You already have data saved for this service.    ")
        choice = input("Do you want to change your passowrd? (y/n)  ")
        while choice.lower() != "n" and choice.lower() != "y":
            choice = input("Please enter y/n:   ")
        if choice.lower() == "y":
            update_password()
            return
        else:
            return

    while password is None:
        password_choice = input("Enter your password or hit enter for a random one: ")
        if password_choice == "":
            password_choice = password_generator()
            print("Generated:", password_choice)
            confirm = input("Is this okay? (y/n)    ")
            while confirm.lower() not in ("y", "n"):
                confirm = input("Please enter y or n:   ")
            if confirm.lower() == "y":
                password = password_choice
        elif is_password_valid(password_choice):
            password = password_choice
        else:
            print("""
Password Conditions:
            
- Only upper- and lowercase letter
- 0-9 digits
- !+-.,#?$%* are allowed
- min. 8 characters
            
            """)

    while username == None or username_choice == "n":                
        username = input("Lastly your username/email:   ")
        while username == "":
            username = input("Username/email can't be empty. Please retry: ")
        print("Your input: ", username)
        username_choice = input("Just to confirm click enter or if not hit n")
        while username_choice.lower() != "" and username_choice.lower() != "n":
            username_choice = input("Please hit enter OR n, Thanks!    ")
        if username_choice == "":
            print("Great, now thats finished too!")
         

    safe[service] = {"username": username, "password": password}
    save_to_file()
    print(f"""
        Service: {service}
        Username: {username}  
        Password: {password}

        Succesfully saved!
    """)


# Updaten eines Password/Username
def update_password():
    service = input("For which service do you want to change your login credentials?    ")
    while service == "":
        service = input("You can't enter an empty input.    ")

    while service not in safe:
        print(f"There is no such service as {service}")
        service = input("Please enter an existing service or enter quit to leave the programm:  ")
        if service.lower() == "quit":
            return
    print(f"""
    {service}:

    Username: {safe[service]["username"]}
    Password: {safe[service]["password"]}

    """)



    print("""
What do you want to change?

1 - Username/email
2 - Password
3 - Both
""")
    choice = input("Your choice:    ")

    while choice != "1" and choice != "2" and choice != "3":
        choice = input("Please enter 1, 2 or 3:  ")

    if choice in ("1","3"):
        print("Your current username/email: ", safe[service]["username"])
        username = input("What shall your changed login credential be?\n")
        if username == "":
            username = "[no username/email given]"
        safe[service]["username"] = username
        save_to_file()
        print(f"Succesfully changed your username/email to {username}")


    if choice in ("2","3"):
        print("Your current password: ", safe[service]["password"])
        password_confirmed = False
        
        while not password_confirmed:
            password_choice = input("Do you want to change it for a random generated one? (y/n)    ")
            while password_choice.lower() != "y" and password_choice.lower() != "n":
                password_choice = input("Please enter either n or y:    ")
            
            if password_choice.lower() == "y":
                password = password_generator()
                final_password_choice = input(f"New password is {password}, is this alright? (y/n)")
                while final_password_choice.lower() != "y" and final_password_choice.lower() != "n":
                    final_password_choice = input("Please enter either y or n:    ")
                
                if final_password_choice.lower() == "y":
                    password_confirmed = True
            else:
                while not password_confirmed:
                    password = input("Please enter your desired password:   ")
                    if not is_password_valid(password):
                        print("""
Password Conditions:
- Only upper- and lowercase letter
- 0-9 digits
- !+-.,#?$%* are allowed
- min. 8 characters
                    
                    """)
                    else:
                        password_confirmation = input("Please repeat it to confirm:    ")
                        if password_confirmation != password:
                            print("The passwords don't match")
                        else:
                            password_confirmed = True

        safe[service]["password"] = password
        save_to_file()
        print("Great, password confirmed and saved!")    


load_from_file()
add_password()                    
update_password()            