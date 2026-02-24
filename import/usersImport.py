import json, os
from db import User

path = "C:/session_chmpion/sesseion main/session 1/Приложение Ресурсы/Ресурсы/Import/users"

for i in os.listdir(path):
    with open(f"{path}/{i}","r",encoding="utf-8") as file:
        data = json.load(file)
        User.create(id=data['id'],
                    full_name=data["full_name"],
                    is_manager=data['is_manager'],
                    is_engineer=data["is_engineer"],
                    phone=data["phone"],
                    is_operator=data["is_operator"],
                    role=data["role"]
                    )
    