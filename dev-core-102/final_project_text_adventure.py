import json
import os
import random

def save_game(game_state):
    with open('dev-core-102/game_state.json', 'w') as f:
        json.dump(game_state, f, indent=4)
    print("Игра сохранена.")

def load_game():
    if os.path.exists('dev-core-102/game_state.json'):
        with open('dev-core-102/game_state.json', 'r') as f:
            game_state = json.load(f)
        print("Игра загружена.")
        return game_state
    else:
        print("Не найдено сохранение.")
        return None

def display_game_state(game_state):
    print(f"\nТекущая локация: {game_state['location']}")
    print(f"Здоровье: {game_state['health']}")
    print(f"Инвентарь: {', '.join(game_state['inventory']) if game_state['inventory'] else 'Нет предметов'}\n")


def start_game():
    game_state = {
        'location': 'начало',
        'health': 100,
        'inventory': [],
        'visited_locations': ['начало'],
    }
    print("Ты стоишь на развилке. Куда ты пойдешь? К реке или в горы?")
    game_loop(game_state)

def game_loop(game_state):
    while True:
        display_game_state(game_state)
        
        print("Что ты будешь делать?")
        print("1. Пойти к реке.")
        print("2. Пойти в горы.")
        print("3. Сохранить игру.")
        print("4. Загрузить игру.")
        print("5. Выйти из игры.")
        
        choice = input("Выбери действие (1, 2, 3, 4, 5): ")
        
        if choice == "1":
            go_to_river(game_state)
        elif choice == "2":
            go_to_mountains(game_state)
        elif choice == "3":
            save_game(game_state)
        elif choice == "4":
            saved_game_state = load_game()
            if saved_game_state:
                game_state = saved_game_state
        elif choice == "5":
            print("Спасибо за игру!")
            break
        else:
            print("Неверный выбор. Попробуй снова.")


def go_to_river(game_state):
    print("\nТы направляешься к реке. Вдруг ты видишь огромную тень, и из воды появляется Ктулху!")
    fight(game_state, "Ктулху")

def go_to_mountains(game_state):
    print("\nТы решаешь пойти в горы. Внезапно, из-за камней, появляется медведь и нападает!")
    fight(game_state, "медведь")

def fight(game_state, enemy_name):
    if enemy_name == "Ктулху":
        enemy_health = random.randint(50, 100) 
        print(f"\nТы сражаешься с мифическим существом {enemy_name}! У него {enemy_health} здоровья.")
    else:
        enemy_health = random.randint(30, 60)  

    while game_state['health'] > 0 and enemy_health > 0:
        print(f"\nТвои здоровье: {game_state['health']}, {enemy_name} здоровье: {enemy_health}")
        print("Что ты будешь делать?")
        print("1. Атаковать.")
        print("2. Использовать предмет из инвентаря.")
        
        choice = input("Выбери действие (1 или 2): ")
        
        if choice == "1":
            attack_damage = random.randint(10, 20)
            print(f"\nТы наносишь {attack_damage} урона {enemy_name}.")
            enemy_health -= attack_damage
            if enemy_health <= 0:
                print(f"\nТы победил {enemy_name}!")
                game_state['inventory'].append('зелье')  
                break
            
            enemy_attack = random.randint(5, 15)
            print(f"{enemy_name} атакует тебя, нанося {enemy_attack} урона.")
            game_state['health'] -= enemy_attack
            if game_state['health'] <= 0:
                print("\nТы погиб. Игра окончена.")
                break
                
        elif choice == "2":
            use_inventory(game_state)
        else:
            print("Неверный выбор. Попробуй снова.")

def use_inventory(game_state):
    if not game_state['inventory']:
        print("Инвентарь пуст. Нечего использовать.")
        return
    
    print("\nВ твоем инвентаре следующие предметы:")
    for i, item in enumerate(game_state['inventory'], 1):
        print(f"{i}. {item}")
    
    choice = input("Выбери предмет для использования (введи номер): ")

    try:
        choice = int(choice)
        if 1 <= choice <= len(game_state['inventory']):
            item = game_state['inventory'][choice - 1]
            print(f"\nТы использовал {item}.")
            if item == 'зелье':
                print("Ты использовал зелье, и он восстанавливает тебе немного здоровья!")
                game_state['health'] = min(game_state['health'] + 20, 100) 
            else:
                print(f"Использование {item} не имеет эффекта.")
        else:
            print("Неверный выбор.")
    except ValueError:
        print("Пожалуйста, введи номер предмета.")

def main():
    print("Хотите начать новую игру или загрузить сохранение? (n для новой игры, l для загрузки)")
    choice = input()

    if choice.lower() == "l":
        game_state = load_game()
        if game_state:
            game_loop(game_state)
        else:
            print("Начинаем новую игру...")
            start_game()
    elif choice.lower() == "n":
        start_game()
    else:
        print("Неверный выбор. Начинаем новую игру...")
        start_game()

if __name__ == "__main__":
    main()
