import os

def save_recipes_to_file(recipes, filename):
    if not recipes:
        print("Нет рецептов для сохранения.")
        return
    
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for recipe, ingredients in recipes.items():
                if recipe and ingredients:
                    ingredients_str = ', '.join(ingredients)
                    file.write(f'{recipe}: {ingredients_str}\n')
                else:
                    print(f"Пропущен рецепт: {recipe}, ингредиенты: {ingredients}")
        print("Рецепты сохранены в файл.")
    except Exception as e:
        print(f"Ошибка при записи в файл: {e}")

def load_recipes_from_file(filename):
    recipes = {}
    if not os.path.exists(filename):
        print("Файл не существует.")
        return recipes
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    recipe_name, ingredients_str = line.strip().split(': ', 1)
                    ingredients = [ingredient.strip() for ingredient in ingredients_str.split(',')]
                    recipes[recipe_name.strip()] = ingredients
                except ValueError:
                    print(f"Ошибка в формате данных в файле: {line.strip()}")
    except Exception as e:
        print(f"Ошибка при загрузке данных из файла: {e}")
    
    print("Рецепты загружены из файла.")
    return recipes

def display_recipes(recipes):
    if not recipes:
        print("Нет загруженных рецептов.")
        return
    print("Рецепты:")
    for recipe, ingredients in recipes.items():
        print(f"- {recipe}: {', '.join(ingredients)}")

def is_valid_recipe_name(name):
    return len(name.strip()) > 0

def is_valid_ingredients(ingredients_str):
    ingredients = ingredients_str.split(',')
    return len(ingredients) > 0 and all(ingredient.strip() for ingredient in ingredients)

def add_or_update_recipe(recipes):
    while True:
        recipe_name = input("Введите название рецепта: ").strip()
        if not is_valid_recipe_name(recipe_name):
            print("Ошибка: название рецепта не может быть пустым.")
            continue
        
        ingredients_str = input("Введите ингредиенты через запятую: ").strip()
        if not is_valid_ingredients(ingredients_str):
            print("Ошибка: должны быть указаны хотя бы одни ингредиенты.")
            continue

        ingredients = [ingredient.strip() for ingredient in ingredients_str.split(',')]
        
        print(f"Вы уверены, что хотите сохранить рецепт '{recipe_name}' с ингредиентами: {', '.join(ingredients)}? (да/нет)")
        confirmation = input().strip().lower()
        if confirmation == 'да':
            recipes[recipe_name] = ingredients
            print(f"Рецепт '{recipe_name}' добавлен или обновлен.")
            break
        else:
            print("Пожалуйста, попробуйте снова.")
            continue
    
    return recipes

def main():
    recipes = {}
    filename = 'dev-core-102/recipes.txt'

    while True:
        print("\nМеню:")
        print("1. Сохранить рецепты в файл")
        print("2. Загрузить рецепты из файла")
        print("3. Показать загруженные рецепты")
        print("4. Добавить или обновить рецепт")
        print("5. Выход")
        
        choice = input("Выберите действие (1-5): ")

        if choice == '1':
            save_recipes_to_file(recipes, filename)
        elif choice == '2':
            recipes = load_recipes_from_file(filename)
        elif choice == '3':
            display_recipes(recipes)
        elif choice == '4':
            recipes = add_or_update_recipe(recipes)
        elif choice == '5':
            print("Выход из программы.")
            break
        else:
            print("Некорректный выбор. Пожалуйста, выберите действие от 1 до 5.")

if __name__ == '__main__':
    main()
