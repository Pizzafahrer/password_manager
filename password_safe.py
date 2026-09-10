import random
import string

# Hier wird alles drinnen gespeichert, später dann in einer json
safe = {}

# alle möglichen characters
possible_chars = string.ascii_lowercase + string.ascii_uppercase + string.digits + "!+-.,#?$%*"


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
        print("You already have a password for this service.    ")
        choice = input("Do you want to change your passowrd? (y/n)  ")
        while choice.lower() != "n" and choice.lower() != "y":
            choice = input("Please enter y/n:   ")
        if choice.lower() == "y":
            update_password()
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
            print("Only uppercase, lowercase, 0-9, !+-.,#?$%* and min. 8 characters.    ")

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
    print(f"""
        Service: {service}
        Username: {username}  
        Password: {password}

        Succesfully saved!
    """)
    
add_password()

# Updaten eines Password/Username
def update_password():
    pass
