import json
from db import Item

with open("C:/session_chmpion/sesseion main/session 1/Приложение Ресурсы/Ресурсы/Import/products.json","r",encoding="utf-8") as file:
    spis = json.load(file)
    Item.insert_many(spis).execute()