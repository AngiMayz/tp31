from datetime import datetime
import os
import json
from auth import load_user_data, save_user_data

def add_payment(username, category, purpose, quantity, price, date=None):
    payment = {
        "category": category,
        "purpose": purpose,
        "quantity": quantity,
        "price": price,
        "total": quantity * price,
        "date": date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    data = load_user_data(username)
    data["payments"].append(payment)
    save_user_data(username, data)

def delete_payment(username, index):
    data = load_user_data(username)
    if 0 <= index < len(data["payments"]):
        removed = data["payments"].pop(index)
        save_user_data(username, data)
        return removed
    return None

def get_payments(username):
    data = load_user_data(username)
    payments = data.get("payments", [])
    
    for p in payments:
        if isinstance(p["date"], int):  # Если дата — число
            try:
                p["date"] = datetime.fromtimestamp(p["date"]).strftime("%Y-%m-%d %H:%M:%S")
            except Exception as e:
                print(f"Ошибка при преобразовании даты: {e}")
                p["date"] = "Неизвестная дата"
                
    return payments

def save_user_data(username, data):
    with open(os.path.join("users", f"{username}.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
def load_user_data(username):
    try:
        with open(os.path.join("users", f"{username}.json"), "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл {username}.json не найден.")
        return {"password": "", "payments": []}
    except json.JSONDecodeError:
        print(f"Ошибка в формате JSON для {username}.json")
        return {"password": "", "payments": []}

def add_test_payments(username):
    test_payments = [
        {
            "category": "Продукты",
            "purpose": "Хлеб",
            "quantity": 2,
            "price": 30,
            "total": 60,
            "date": "2016-11-01"
        },
        {
            "category": "Продукты",
            "purpose": "Молоко",
            "quantity": 1,
            "price": 70,
            "total": 70,
            "date": "2016-11-01"
        },
        {
            "category": "Транспорт",
            "purpose": "Бензин",
            "quantity": 1,
            "price": 500,
            "total": 500,
            "date": "2016-11-30"
        },
        {
            "category": "Медицина",
            "purpose": "Анализы",
            "quantity": 1,
            "price": 1200,
            "total": 1200,
            "date": "2016-11-01"
        },
        {
            "category": "Разное",
            "purpose": "Книга",
            "quantity": 1,
            "price": 450,
            "total": 450,
            "date": "2016-11-04"
        }
    ]

    data = load_user_data(username)
    data["payments"].extend(test_payments)
    save_user_data(username, data)