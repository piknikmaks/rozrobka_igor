import os
import time
import msvcrt
from storage import save_state, load_state

last_save = None

class System:
    def clear(self):
        os.system("cls")

class Character(System):
    def __init__(self, name="Name", money=0, level=1, hp=1, wins=0, defeats=0, inv=None):
        self.name = name
        self.money = money
        self.level = level
        self.hp = hp
        self.wins = wins
        self.defeats = defeats
        self.inv = inv if inv is not None else {}

    def stats(self):
        print(f"Монети: {self.money}")
        print(f"Рівень: {self.level}")
        print(f"HP: {self.hp}")
        print(f"Інвентар: {self.inv}")
        
        print(f"Перемоги: {self.wins}")
        print(f"Поразки: {self.defeats}")

    def check_char(self):
        if self.level > 10:
            print("\nВи готові до великої битви!")
        elif self.level > 5:
            print("\nВи на шляху до майстра")
        elif self.level <= 5:
            print("\nТренуйтесь більше!")

    def big_battle(self):
        if self.hp > 50:
            self.wins += 1
            player.clear()
            self.stats()
            print("\nПеремога!")
            last_save = save_state(player)
        elif self.hp > 30:
            self.wins += 1
            self.hp -= 30
            player.clear()
            self.stats()
            print("\nПеремога, але ви отримали рани")
            print(f"Поточний HP: {self.hp}")
            last_save = save_state(player)
        elif self.hp <= 30:
            self.defeats += 1
            self.money = 0
            self.hp = 1
            player.clear()
            self.stats()
            print("\nПоразка...")
            last_save = save_state(player)
    
    def shop(self):
        while True:     
            player.clear()
            player.stats()       
            print("\nДоступні товари:")
            available_count = 0
            for key, item in shop_products.items():
                if item.price <= player.money:
                    print(f"{key}. {item.name} — {item.price} монет")
                    available_count += 1

            if available_count == 0:
                print("\nУ вас замало грошей на будь-який товар. Повертайтеся пізніше!")
                break
            
            shop_choice = int(input("\nВведіть ID товару, який хочете купити:\n"))
            player.buy_item(shop_choice)
            last_save = save_state(player)

            print(f"\nУ вас лишилось {self.money} монет")
            
            repeat = input("\nХочете придбати ще щось? (y / n): ").strip().lower()
            
            if repeat == "y":
                continue
            break

class Player(Character):
    def add_money(self):        
        self.money += int(self.level * 1.5)

    def buy_item(self, item_id):
        player.clear()
        player.stats()
        item = shop_products.get(item_id)
        if item and self.money >= item.price:
            self.money -= item.price
            
            found = False
            for inv_item in self.inv:
                if inv_item.name == item.name:
                    self.inv[inv_item] += 1
                    found = True
                    break
            
            if not found:
                self.inv[item] = 1
            print(f"\nВи купили {item.name}!")
        else:
            print("\nНедостатньо грошей або невірний ID!")

    def use_item(self):
        while True:
            player.clear()
            player.stats()

            potions = [
                (item, count) for item, count in self.inv.items()
                if isinstance(item, Potion)
            ]

            if not potions:
                print("\nУ вас немає зілля в інвентарі")
                input("Натисніть Enter, щоб повернутися....")
                break

            print("\n Доступні зілля:")
            for i, (item, count) in enumerate(potions, 1):
                print(f"{i}. {item.name}: {item.heal}HP - {count} шт.")

            try:
                choice = int(input("\nЯке зілля використати? (введіть номер): "))
                if 1 <= choice <= len(potions):
                    selected_potion, count = potions[choice - 1]

                    self.hp += selected_potion.heal
                    self.inv[selected_potion] -= 1
                    if self.inv[selected_potion] <= 0:
                        del self.inv[selected_potion]

                    print(f"\nВикористано {selected_potion.name}")
                    print(f"Відновлено {selected_potion.heal}HP")
                else:
                    print("Невірний номер.")
            except ValueError:
                print("Будь ласка, введвіть число.")
            
            last_save = save_state(player)
            
            choice = input("\nЧи хочете ви використати ще зілля? (y / n):\n").strip().lower()
            if choice == "y":
                continue
            break

    def calculate_damage(self):
        base_damage = self.level * 2
        weapon_damage = 0

        for item, count in self.inv.items():
            if isinstance(item, Weapon):
                weapon_damage += item.damage * count

        total_damage = base_damage + weapon_damage
        return total_damage

class Enemy(Character):
    def __init__(self, name, hp, damage, money_drop, lvl_drop):
        super().__init__(name, hp)
        self.damage = damage
        self.money_drop = money_drop
        self.lvl_drop = lvl_drop
        self.max_hp = hp
        
    def enemy_info(self):
        self.hp = self.max_hp
        return f"{self.name}: {self.max_hp} HP, {self.damage} DMG, {self.money_drop}$, {self.lvl_drop}XP"

    def fight(self, player):
        self.hp = self.max_hp
        
        print(f"\nБій почався! {player.name} нападає на {self.name}!")
        
        while self.hp > 0 and player.hp > 0:
            damage_to_enemy = self.calculate_damage()
            self.hp -= damage_to_enemy
            print(f"Ви вдарили {self.name} на {damage_to_enemy}! У нього залишилось {self.hp}.")
        
            if self.hp <= 0:
                print(f"\nВи перемогли!")
                player.money += self.money_drop
                player.level += self.lvl_drop
                player.wins += 1
                return True
            
            player.hp -= self.damage
            print(f"{self.name} вдарив вас на {self.damage}! У вас залишилось {player.hp}.")
            
            if player.hp <= 0:
                print(f"\nВи програли....")
                player.money = 0
                player.defeats += 1
                return False

class Item:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class Weapon(Item):
    def __init__(self, name, price, damage):
        super().__init__(name, price)
        self.damage = damage

class Shield(Item):
    def __init__(self, name, price, block):
        super().__init__(name, price)
        self.block = block

class Potion(Item):
    def __init__(self, name, price, heal):
        super().__init__(name, price)
        self.heal = heal

default_state = {
    "player_name": "",
    "level": 1,
    "coins": 0,
    "hp": 1,
    "wins": 0,
    "defeats": 0,
    "inventory": {},
    "settings": {"difficulty": "normal"}
}

enemies = [
    Enemy("Русня", 1, 1, 1, 0),
    Enemy("Слимак", 20, 5, 5, 1),
    Enemy("Скелет", 40, 10, 20, 2),
    Enemy("Дикий кабан", 60, 12, 35, 3),
    
    Enemy("Розбійник", 100, 18, 60, 10),
    Enemy("Орк-піхотинець", 150, 25, 120, 15),
    Enemy("Темний магістр", 120, 35, 200, 25),
    
    Enemy("Гірський троль", 350, 40, 400, 50),
    Enemy("Дракон", 600, 60, 1500, 150),
    Enemy("Рицар Смерті", 1000, 85, 5000, 500)
]

shop_products = {
    1: Weapon("Іржавий ніж", 25, 5),
    2: Weapon("Залізний меч", 100, 25),
    3: Weapon("Палаючий дворучник", 500, 150),
    
    4: Shield("Стара кришка", 20, 2),
    5: Shield("Дерев'яний щит", 50, 10),
    6: Shield("Лицарський баклер", 125, 30), #Щити не працюють
    
    7: Potion("Мале зілля", 15, 15),
    8: Potion("Зілля лікування", 40, 40),
    9: Potion("Еліксир відновлення", 100, 100)
}

player = Player()

current_state = load_state("game_save.json", default_state)

player.name = current_state["player_name"]
player.money = current_state["coins"]
player.level = current_state["level"]
player.hp = current_state["hp"]
player.wins = current_state["wins"]
player.inv = current_state["inventory"]

if not player.name:
    u_name = str(input("\nВітаємо, введіть своє ім'я: "))
    player.name = u_name

print(f"Ласкаво просимо, {player.name}!\n")

while True:
    player.stats()

    print("\nВи можете:")
    print("1. Заробити гроші.")
    print("2. Використати витратні матеріали.")
    print("3. Скористатися магазином.")
    print("4. Перевірити готовність до битви.")
    print("5. Взяти участь у великій битві.")
    print("6. Викликати на дуель.")
    print("7. Вийти.")

    choice = str(input("\nОберіть пункт: ")).strip()

    if choice == "1":
        while True:
            player.clear()
            player.stats()
            print(f"\nНатискайте Enter, щоб заробити {int(player.level*1.5)} монет; exit - щоб вийти\n")
            add_money = input("\n").strip()
            
            if add_money == "exit":
                last_save = save_state(player)
                break
            else:
                while msvcrt.kbhit():
                    msvcrt.getch()

                player.add_money()
                time.sleep(0.1)
                continue
    elif choice == "2":
        player.clear()
        player.stats()
        player.use_item()
    elif choice == "3":
        player.clear()
        player.stats()
        player.shop()
    elif choice == "4":
        player.clear()
        player.stats()
        player.check_char()
    elif choice == "5":
        player.clear()
        player.stats()
        player.big_battle()
    elif choice == "6":
        player.clear()
        player.stats()
        
        print("\nВсі доступні вороги:")
        
        for i, enemy in enumerate(enemies, 1):
            print(f"{i}. {enemy.enemy_info()}")

        print("\nЗверніть увагу, якщо ви програєте дуель ви втратите всі монети та HP")
        while True:
            try:
                e_choice = int(input("\nВведіть номер ворога: "))
                if 1 <= e_choice <= len(enemies):
                    selected_enemy = enemies[e_choice - 1]
                    
                    player.clear()
                    player.stats()
                    
                    print(f"\nВи викликали на бій: {selected_enemy.name}!")
                    selected_enemy.fight(player)
                    last_save = save_state(player)
                    break
                else:
                    raise ValueError("\nНеіснуючий номер.")
            except ValueError:
                print("\nНевірний вибір.")
                continue
    elif choice == "7":
        break
    else:
        print("Невірний вибір")
        input("Натисніть Enter для продовження....")
        player.clear()
        continue

    back = input("\nПовернутися в меню? (y / n): ").strip().lower()
    if back == "y":
        player.clear()
        continue
    else:
        choice = str(input("\nЗберегти прогрес? (y / n): ")).strip().lower()
        
        try:
            if choice == "y":
                last_save = save_state(player)
            else:
                break
        except ValueError:
                print("\nНевірний вибір.")
                continue
        break
input("Натисніть Enter для закриття програми.")