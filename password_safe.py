import secrets  #für password generator
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
    password = "".join(secrets.choice(possible_chars) for _ in range(secrets.randbelow(max_chars -min_char + 1) + min_char))
    return password

#print(password_generator())

#check ob password in valid is
def is_password_valid(password, min_length=8):
    if len(password) < min_length:
        return False
    if not set(password).issubset(set(possible_chars)):
        return False
    return True


def show_password_conditions():
    return """
Password Conditions:

- Only upper- and lowercase letters
- 0-9 digits
- !+-.,#?$%* are allowed
- min. 8 characters
"""

    
#Hinzufügen von einem Password
def create_password():

    if "show_overwrite" not in st.session_state:
        st.session_state.show_overwrite = False

    service = st.text_input("Service(casesensitive): ").strip()
    username = st.text_input("Username/Email:").strip()
    password = st.text_input("Password:", type="password").strip()
    password_confirm = st.text_input("Confirm password:", type="password").strip()

    if st.button("Save:"):
        if service == "":
            st.error("Service can't be empty!")
        elif username == "":
            st.error("Username/Email can't be empty!")
        elif password == "" or password_confirm == "":
            st.error("Password can't be empty!")
        elif not is_password_valid(password):
            st.error("The password isn't valid.")
            st.text(show_password_conditions())
        elif password != password_confirm:
            st.error("The passwords don't match!")
        elif service in safe:
            st.warning(f"An entry for '{service}' already exists.")
            st.session_state.show_overwrite = True
        else:
            safe[service] = { "username": username, "password": encrypt_password(password)}
            save_to_file()
            st.success("Successfully saved!")

    if st.session_state.show_overwrite:
        overwrite = st.checkbox("Overwrite existing entry?")

        if overwrite:
            safe[service] = {"username": username, "password": encrypt_password(password)}
            save_to_file()
            st.success("Successfully overwritten!")
            st.session_state.show_overwrite = False
            st.rerun()



def dashboard():
    if "show_password" not in st.session_state:
        st.session_state.show_password = None
    if "delete_confirm" not in st.session_state:
        st.session_state.delete_confirm = None
    if "edit_username" not in st.session_state:
        st.session_state.edit_username = None
    if "edit_password" not in st.session_state:
            st.session_state.edit_password = None
    for i in safe:
        caption = False
        with st.expander(i):
            col1, col2, col3 = st.columns([2, 3, 1], vertical_alignment="center")
            with col1:
                st.write("Username/Email:")
            with col2:
                if st.session_state.edit_username == i:
                    username = st.text_input("New username:", value=safe[i]["username"], key=f"btw_new_username{i}")
                    col4, col5 = st.columns([1,2])
                    with col4:
                        if st.button("Save", key=f"btn_username{i}"):
                            if not username == "":
                                safe[i]["username"] = username
                                save_to_file()
                                st.session_state.edit_username = None
                                st.rerun()
                            else:
                                with col5:
                                    st.caption("Username/Email can't be empty!")
                else:
                    st.markdown(f"`{safe[i]['username']}`")
            with col3:
                is_editing = st.session_state.edit_username == i
                buttonchange = "Cancel" if is_editing else "Change"
                if st.button(buttonchange, key= f"btn_up{i}"):
                    if is_editing:
                        st.session_state.edit_username = None
                    else:
                        st.session_state.edit_username = i
                    st.rerun()

#password teil
            col1, col2, col3 = st.columns([2,3,1], vertical_alignment = "center")
            with col1:
                st.write("Password:")
            with col2:
                if st.session_state.edit_password == i:
                    password = st.text_input("New password:", type="password", value=decrypt_password(safe[i]["password"]), key =f"btn_new_password{i}") 
                    col4,col5 = st.columns([1,2])
                    with col4:
                        if st.button("Save", key= f"btn_password{i}"):
                            if not is_password_valid(password):
                                with col5:
                                    st.caption("The password isn't valid.")
                                    st.text(show_password_conditions())
                            else:
                                safe[i]["password"] = encrypt_password(password)
                                save_to_file()
                                st.session_state.edit_password = None
                                st.rerun()
                    
                else:
                    if st.session_state.show_password == i:
                        st.markdown(f"`{decrypt_password(safe[i]["password"])}`")
                    else:
                        password_length = "*" * len(decrypt_password(safe[i]["password"]))
                        st.markdown(f"`{password_length}`")
            with col3:
                is_editing = st.session_state.edit_password == i
                buttonchange = "Cancel" if is_editing else "Change"
                if st.button(buttonchange, key= f"btn_down{i}"):
                    if is_editing:
                        st.session_state.edit_password = None
                    else:
                        st.session_state.edit_password = i
                    st.rerun()
                        
#deletion teil
            col1,col2,col3= st.columns([1,5,2], vertical_alignment="center")
            with col1:
                if st.button("Delete", key=f"btn_deletion{i}"):
                    if st.session_state.delete_confirm == i:
                        del safe[i]
                        save_to_file()
                        st.rerun()
                        return
                    else:
                        caption = True

            with col2:
                if st.checkbox("Confirm deletion", key=f"check_deletion{i}"):
                    st.session_state.delete_confirm = i

            with col3:
                if st.button("Show", key=f"btn_show{i}"):
                    if st.session_state.show_password == i:
                        st.session_state.show_password = None
                    else:    
                        st.session_state.show_password = i
                    st.rerun()

            if caption == True:
                st.caption("Please check the textbox on the right.")



load_from_file()
load_or_create_key()
create_password()
dashboard()