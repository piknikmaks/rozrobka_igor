import os
import time
import msvcrt
from core.storage import save_state

class Character:
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
            self.clear()
            self.stats()
            print("\nПеремога!")
            save_state(self)
        elif self.hp > 30:
            self.wins += 1
            self.hp -= 30
            self.clear()
            self.stats()
            print("\nПеремога, але ви отримали рани")
            print(f"Поточний HP: {self.hp}")
            save_state(self)
        elif self.hp <= 30:
            self.defeats += 1
            self.money = 0
            self.hp = 1
            self.clear()
            self.stats()
            print("\nПоразка...")
            save_state(self)
    
    def shop(self):
        while True:     
            self.clear()
            self.stats()       
            print("\nДоступні товари:")
            available_count = 0
            for key, item in SHOP_PRODUCTS.items():
                if item.price <= self.money:
                    print(f"{key}. {item.name} — {item.price} монет")
                    available_count += 1

            if available_count == 0:
                print("\nУ вас замало грошей на будь-який товар. Повертайтеся пізніше!")
                break
            
            shop_choice = int(input("\nВведіть ID товару, який хочете купити:\n"))
            self.buy_item(shop_choice)
            save_state(self)

            print(f"\nУ вас лишилось {self.money} монет")
            
            repeat = input("\nХочете придбати ще щось? (y / n): ").strip().lower()
            
            if repeat == "y":
                continue
            break

    def clear(self):
        os.system("cls")

class Player(Character):
    def add_money(self):        
        self.money += int(self.level * 1.5)

    def buy_item(self, item_id):
        self.clear()
        self.stats()
        item = SHOP_PRODUCTS.get(item_id)
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
            self.clear()
            self.stats()

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
            
            save_state(self)
            
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
    
    def calculate_reduction(self):
        shield_reduction = 0

        for item, count in self.inv.items():
            if isinstance(item, Shield):
                shield_reduction += item.block * count
                
        return shield_reduction

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
            shield_block = self.calculate_reduction()
            player_damage = self.calculate_damage()
            self.hp -= player_damage
            print(f"Ви вдарили {self.name} на {player_damage}! У нього залишилось {self.hp}.")
        
            if self.hp <= 0:
                print(f"\nВи перемогли!")
                player.money += self.money_drop
                player.level += self.lvl_drop
                player.wins += 1
                return True
            
            enemy_damage = self.damage - shield_block
            
            if enemy_damage < 1:
                enemy_damage = 0
            
            player.hp -= enemy_damage
            print(f"{self.name} вдарив вас на {enemy_damage}! У вас залишилось {player.hp}.")
            
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


ENEMIES = [
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

SHOP_PRODUCTS = {
    1: Weapon("Іржавий ніж", 25, 5),
    2: Weapon("Залізний меч", 100, 25),
    3: Weapon("Палаючий дворучник", 500, 150),
    
    4: Shield("Стара кришка", 20, 2),
    5: Shield("Дерев'яний щит", 50, 10),
    6: Shield("Лицарський баклер", 125, 30),
    
    7: Potion("Мале зілля", 15, 15),
    8: Potion("Зілля лікування", 40, 40),
    9: Potion("Еліксир відновлення", 100, 100)
}