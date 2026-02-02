import os

money = 0
level = 1
hp = 1
wins = 0
defeats = 0

inv = []

def stats():
    print(f"Монети: {money}")
    print(f"Рівень: {level}")
    print(f"HP: {hp}")
    print(f"Інвентар: {inv}")
    
    print(f"Перемоги: {wins}")
    print(f"Поразки: {defeats}")
    
def clear():
    os.system("cls")

print("Ласкаво просимо!\n")

while True:
    stats()
    
    print("\nВи можете:")
    print("1. Додати монет та скористатися магазином.")
    print("2. Додати рівень та перевірити готовність до битви.")
    print("3. Додати HP та взяти участь у битві.")
    print("4. Переглянути інвентар.")
    
    choise = str(input("\nОберіть пункт: ")).strip()
    
    if choise == "1":
        clear()
        stats()
        
        while True:
            try:
                change = int(input("\nДодайте або відніміть монети: "))
            except ValueError:
                print("Введіть число")
                continue
            
            if money + change < 0:
                print("Недостатньо монет. Баланс не може бути від'ємним!")
                continue
            
            money += change
            clear()
            stats()
            print(f"\nВи отримали монети. Монет: {money}")
            break
        
        while True:
            clear()
            stats()
            
            if money >= 100:
                print("\nВи можете придбати меч, щит або зілля.")

                allowed = {"sw", "sh", "po"}

                while True:
                    sel1 = str(input("Введіть:\n - sw, якщо хочете придбати меча;\n - sh, якщо хочете придбати щит; \n - po, якщо хочете придбати зілля.\n\n")).strip().lower()

                    try:
                        if sel1 not in allowed:
                            raise ValueError("Недоступне значення.")
                    except ValueError:
                        print("\nПомилка! Введіть один з доступних варіантів.")
                        continue
                    else:
                        break

                if sel1 == "sw":
                    money -= 100
                    inv.append("Меч")
                    clear()
                    stats()
                    print("\nВи успішно придбали меч!")
                elif sel1 == "sh":
                    money -= 50
                    inv.append("Щит")
                    clear()
                    stats()
                    print("\nВи успішно придбали щит!")
                elif sel1 == "po":
                    money -= 25
                    inv.append("Зілля")
                    clear()
                    stats()
                    print("\nВи успішно придбали зілля!")
            elif money >= 50:
                print("\nВи можете придбати щит або зілля.")

                allowed = {"sh", "po"}

                while True:
                    sel1 = str(input("Введіть:\n - sh, якщо хочете придбати щит; \n - po, якщо хочете придбати зілля.\n\n")).strip().lower()

                    try:
                        if sel1 not in allowed:
                            raise ValueError("Недоступне значення.")
                    except ValueError:
                        print("\nПомилка! Введіть один з доступних варіантів.")
                        continue
                    else:
                        break
                if sel1 == "sh":
                    money -= 50
                    inv.append("Щит")
                    clear()
                    stats()
                    print("\nВи успішно придбали щит!")
                elif sel1 == "po":
                    money -= 25
                    inv.append("Зілля")
                    clear()
                    stats()
                    print("\nВи успішно придбали зілля!")
            elif money < 50 and money > 25:
                print("\nВи можете придбати зілля.")

                allowed = {"po"}

                while True:
                    sel1 = str(input("Введіть:\n - po, якщо хочете придбати зілля.\n\n")).strip().lower()

                    try:
                        if sel1 not in allowed:
                            raise ValueError("Недоступне значення.")
                    except ValueError:
                        print("\nПомилка! Введіть один з доступних варіантів.")
                        continue
                    else:
                        break
                if sel1 == "po":
                    money -= 25
                    inv.append("Зілля")
                    clear()
                    stats()
                    print("\nВи успішно придбали зілля!")
            else:
                print("У вас недостатньо монет, щоб купити хоч щось!")
                break

            print(f"У вас лишилось {money} монет")
            
            repeat = input("Хочете придбати ще щось? (y / n): ").strip().lower()
            
            if repeat == "y":
                continue
            break
    elif choise == "2":
        clear()
        stats()
        
        while True:
            try:
                change = int(input("\nДодайте або відніміть рівень: "))
            except ValueError:
                print("Введіть число")
                continue
            
            if level + change < 1:
                print("\nЗанадто низький рівень. Рівень не може бути менше 1.")
                continue
            
            clear()
            stats()
            level += change
            print(f"\nНовий рівень! Поточний рівень: {level}")
            break
        
        if level > 10:
            print("\nВи готові до великої битви!")
        elif level > 5:
            print("\nВи на шляху до майстра")
        elif level <= 5:
            print("\nТренуйтесь більше!")
    elif choise == "3":
        clear()
        stats()
        while True:
            try:
                change = int(input("\nДодайте або відніміть HP: "))
            except ValueError:
                print("Введіть число")
                continue
            
            if hp + change < 1:
                print("\nЗанадто низький HP. HP не може бути менше 1.")
                continue
            
            hp += change
            print(f"\nПоповнено запас HP: {hp}")
            input("Натисніть Enter, щоб перейти до великої битви....")
            break
        
        if hp > 50:
            wins += 1
            clear()
            stats()
            print("\nПеремога!")
        elif hp > 30:
            wins += 1
            hp -= 30
            clear()
            stats()
            print("\nПеремога, але ви отримали рани")
            print(f"Поточний HP: {hp}")
        elif hp <= 30:
            defeats += 1
            money = 0
            hp = 1
            clear()
            stats()
            print("\nПоразка...")
    else:
        print("Невірний вибір")
        continue
    
    back = input("\nПовернутися в меню? (y / n): ").strip().lower()
    if back == "y":
        clear()
        continue
    else:
        break
input("Натисніть Enter для закриття програми.")