import json
import os

def save_state(player):
    path = "game_save.json"
    tmp_path = path + ".tmp"

    inventory_snapshot = {item.name: count for item, count in player.inv.items()}

    game_state = {
        "player_name": player.name,
        "level": player.level,
        "coins": player.money,
        "hp": player.hp,
        "wins": player.wins,
        "defeats": player.defeats,
        "inventory": inventory_snapshot,
        "settings": {
            "difficulty": "normal"
        }
    }

    try:
        with open(tmp_path, 'w', encoding='utf-8') as file:
            json.dump(game_state, file, ensure_ascii=False, indent=2)
        
        os.replace(tmp_path, path)
        
        return True
    except Exception as e:
        print(f"Помилка збереження: {e}")
        
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
            
        return False
    
def load_state(path: str, default: dict) -> dict:
    if not os.path.exists(path):
        return default

    try:
        with open(path, 'r', encoding='utf-8') as file:
            loaded_data = json.load(file)

        if not isinstance(loaded_data, dict):
            return default

        final_state = default.copy()

        for key, default_value in default.items():
            if key in loaded_data:
                val = loaded_data[key]
                is_valid = True
                
                if key in ["level", "coins"]:
                    if not isinstance(val, int) or val < 0:
                        is_valid = False
                elif key == "inventory":
                    if isinstance(val, dict):
                        for item_name, count in val.items():
                            if not isinstance(count, int) or count < 0:
                                is_valid = False
                                break
                    else:
                        is_valid = False
                elif key == "settings":
                    if not isinstance(val, dict):
                        is_valid = False
                if is_valid:
                    final_state[key] = val
                else:
                    print(f"[Валідація] Дані ключа '{key}' некоректні. Скинуто до стандартних.")
            
        return final_state

    except (json.JSONDecodeError, IOError):
        return default