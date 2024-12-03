participants = {}

conference_city = ("Almaty, Kazakhstan")

# Функция для добавления участника
def add_participant():
    name = input("Введите имя участника: ")
    age = input("Введите возраст участника: ")
    email = input("Введите e-mail участника: ")
    
    # Добавляем информацию о участнике в словарь
    participants[name] = {
        "Возраст": age,
        "E-mail": email
    }
    print(f"Участник {name} добавлен!")

# Функция для удаления участника
def remove_participant():
    name = input("Введите имя участника для удаления: ")
    if name in participants:
        del participants[name]
        print(f"Участник {name} удален!")
    else:
        print(f"Участник с именем {name} не найден.")

# Функция для отображения информации о всех участниках
def show_participants():
    if not participants:
        print("Список участников пуст.")
    else:
        for name, info in participants.items():
            print(f"\nИмя: {name}")
            print(f"Возраст: {info['Возраст']}")
            print(f"E-mail: {info['E-mail']}")
    print()

# Функция для отображения координат места проведения
def show_conference_location():
    print(f"Место проведения конференции: Место проведения конференции {conference_city}")
    
# Функция для обновления информации о пользователе
def update_participant():
    name = input("Введите имя участника для обновления: ")
    if name in participants:
        print(f"Обновляем информацию для {name}")
        # Обновление возраста
        new_age = input("Введите новый возраст (оставьте пустым, чтобы не менять): ")
        if new_age:
            participants[name]["Возраст"] = new_age
        
        # Обновление e-mail
        new_email = input("Введите новый e-mail (оставьте пустым, чтобы не менять): ")
        if new_email:
            participants[name]["E-mail"] = new_email

        print(f"Информация для участника {name} обновлена!")
    else:
        print(f"Участник с именем {name} не найден.")


# Главное меню
def main():
    while True:
        print("\nМеню:")
        print("1. Добавить участника")
        print("2. Удалить участника")
        print("3. Показать участников")
        print("4. Показать координаты места проведения")
        print("5. Обновить информацию об участнике")
        print("6. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            add_participant()
        elif choice == "2":
            remove_participant()
        elif choice == "3":
            show_participants()
        elif choice == "4":
            show_conference_location()
        elif choice == "5":
            update_participant()
        elif choice == "6":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор, попробуйте снова.")

# Запуск программы
if __name__ == "__main__":
    main()