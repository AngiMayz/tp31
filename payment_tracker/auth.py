import os
import json
import bcrypt

USERS_DIR = "users"

def ensure_users_dir():
    if not os.path.exists(USERS_DIR):
        os.makedirs(USERS_DIR)

def get_user_files():
    return [f.replace(".json", "") for f in os.listdir(USERS_DIR) if f.endswith(".json")]

def load_user_data(username):
    try:
        with open(os.path.join(USERS_DIR, f"{username}.json"), "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл {username}.json не найден.")
        return {"password": "", "payments": []}
    except json.JSONDecodeError:
        print(f"Ошибка в формате JSON для {username}.json")
        return {"password": "", "payments": []}

def save_user_data(username, data):
    with open(os.path.join(USERS_DIR, f"{username}.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def create_new_user(username, password):
    user_file = os.path.join(USERS_DIR, f"{username}.json")
    if os.path.exists(user_file):
        return False, "Пользователь уже существует"
    if len(password) < 4:
        return False, "Пароль слишком короткий"
    data = {
        "password": hash_password(password),
        "payments": []
    }
    save_user_data(username, data)
    return True, "Пользователь создан"