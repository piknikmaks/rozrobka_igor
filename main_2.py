import os
coins = [33, 25, 91]
money = 0
inventory = ["меч", "щит", "зілля", "амулет", "монети"]
cnt = 0
inv = {
    "меч": "озброєння",
    "щит": "озброєння",
    "зілля": "ліки",
    "амулет": "аксесуар",
    "монети": "валюта"
}
weapons = []
scores = [55, 40, 75, 30, 65, 80, 45, 100]
high = 0

os.system("cls")

print(f"Список монет: {coins}")
for i in range(len(coins)):
    money += coins[i]
    
print(f"\nЗагальна сумма: {money}")
input("Натисніть Enter, щоб перейти до наступного завдання....")

os.system("cls")

for i in range(len(inventory)):
    cnt += 1
    print(f"{cnt}. {inventory[i]}")
    
print(f"\nЗагальна кількість предметів: {cnt}")
input("Натисніть Enter, щоб перейти до наступного завдання....")
os.system("cls")

for i in inv:
    if inv[i] == "озброєння":
        weapons.append(i)

print(f"\nВ вашому інвентарі такі предмети належать до озброєння: {weapons}")
input("Натисніть Enter, щоб перейти до наступного завдання....")
os.system("cls")

for i in range(len(scores)):
    if scores[i] >= 50:
        high += 1
        
print(f"Ваші очки: {scores}")

if high < 2:
    print(f"\nВи набрали більше 50 очок {high} раз")
elif high < 5:
    print(f"\nВи набрали більше 50 очок {high} рази")
elif high >= 5:
    print(f"\nВи набрали більше 50 очок {high} разів")
    
input("Натисніть Enter, щоб перейти до завершення програми....")