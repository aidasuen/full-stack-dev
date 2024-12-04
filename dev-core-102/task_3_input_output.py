# Функция для запроса и обработки данных пользователя
def get_user_info():
    name = input("Введите ваше имя: ")
    
    # Обработка возраста, чтобы он был числом
    while True:
        try:
            age = int(input("Введите ваш возраст: "))
            break
        except ValueError:
            print("Ошибка: возраст должен быть числом. Попробуйте снова.")
    
    favorite_color = input("Введите ваш любимый цвет: ")
    
    return name, age, favorite_color

# Функция для записи данных в файл
def save_user_info(name, age, favorite_color, custom_text):
    file_path = 'dev-core-102/user_info.txt'  # Путь к файлу для сохранения данных
    
    # Записываем данные в файл
    with open(file_path, 'w') as file:
        file.write(f"Имя: {name}\n")
        file.write(f"Возраст: {age}\n")
        file.write(f"Любимый цвет: {favorite_color}\n")
        file.write(f"Текст: {custom_text}\n")  # Добавляем текст, который пользователь введет
    
    print(f"Информация успешно сохранена в файл: {file_path}")

# Функция для чтения данных из файла
def read_user_info():
    file_path = 'user_info.txt'
    
    # Проверяем, существует ли файл
    try:
        with open(file_path, 'r') as file:
            print("\nДанные из файла:")
            print(file.read())
    except FileNotFoundError:
        print("Ошибка: файл с данными не найден.")

def main():
    name, age, favorite_color = get_user_info()
    
    # Запрашиваем дополнительный текст
    custom_text = input("Введите дополнительный текст для записи в файл: ")
    
    # Вывод данных в форматированном виде
    print(f"\nПривет, {name}!")
    print(f"Ваш возраст: {age}")
    print(f"Ваш любимый цвет: {favorite_color}")
    
    # Сохранение информации в файл
    save_user_info(name, age, favorite_color, custom_text)
    
    read_choice = input("\nХотите ли вы прочитать сохранённые данные из файла? (да/нет): ").strip().lower()
    
    if read_choice == 'да':
        read_user_info()
    else:
        print("Хорошо, до свидания!")

if __name__ == "__main__":
    main()
