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
def add_password(service, username, password = None):
    password = None
    while password is None:
        password_choice = input("Enter your password or hit enter for a random one: ")
        if password_choice == "":
            password_choice = password_generator()
            print("Generated:", password_choice)
            confirm = input("Is this okay? (y/n) ")
            while confirm.lower() not in ("y", "n"):
                confirm = input("Please enter y or n: ")
            if confirm.lower() == "y":
                password = password_choice
        elif is_password_valid(password_choice):
            password = password_choice
        else:
            print("Only uppercase, lowercase, 0-9, !+-.,#?$%* and min. 8 characters.")
                    
    
    if service in safe: 
        print("You already have a password for this service.")
        choice = input("Do you want to change your passowrd? (y/n) ")
        while choice.lower() != "n" and choice.lower() != "y":
                    choice = input("Please enter y/n: ")
        if choice.lower() == "y":
            update_password()
        else:
            return


    safe[service] = {"username": username, "password": password}


# Updaten eines Password/Username
def update_password():
    pass




add_password(input("For what service is it used?"), input("What is the username/email for it?"))




# def add_password(password):
#     choice = str(input("Generated or selfmade? (g/s)   "))
#     if choice.lower() == "g":
#         password = password_generator()
#     else:
#           password = str(input("Enter ur password: "))
#           while safe_choice.lower() == "n":
#               password = str(input("Enter ur password: "))
#               safe_choice = str(input("Are you sure? (y/n) "))
#               if safe_choice.lower() == "n":
#                   pass
#               else:
#                   print("New password added")
#                   break
                    
