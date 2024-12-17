import numpy as np

ingredients_list = np.array([
    'Мука', 'Молоко', 'Яйца', 'Сахар', 'Спагетти', 'Томаты', 'Фарш', 'Лук'
])

prices_list = np.array([800, 600, 500, 400, 390, 1000, 3000, 200])

recipes = {
    'Оладьи': ['Мука', 'Молоко', 'Яйца', 'Сахар'],
    'Паста': ['Спагетти', 'Томаты', 'Фарш', 'Лук']
}

def print_recipes_and_prices():
    print("Доступные рецепты и ингредиенты с их стоимостью:")
    for recipe, ingredients in recipes.items():
        print(f"\nРецепт: {recipe}")
        for ingredient in ingredients:
            ingredient_index = np.where(ingredients_list == ingredient)[0]
            if len(ingredient_index) > 0:
                price = prices_list[ingredient_index[0]]
                print(f"  - {ingredient}: {price} тенге")
            else:
                print(f"  - {ingredient}: Цена не найдена")

def add_new_recipe():
    global ingredients_list, prices_list
    new_recipe = input("\nВведите название нового блюда: ").strip()
    ingredients = []

    while True:
        ingredient = input("Введите ингредиент (или 'stop' для завершения): ").strip().lower()
        if ingredient == 'stop':
            break
        ingredients.append(ingredient)

        if ingredient not in ingredients_list:
            price = float(input(f"Введите цену для {ingredient} в тенге: "))
            ingredients_list = np.append(ingredients_list, ingredient)
            prices_list = np.append(prices_list, price)
        else:
            print(f"{ingredient} уже существует, стоимость сохранена: {prices_list[np.where(ingredients_list == ingredient)[0][0]]} тенге")

    recipes[new_recipe] = ingredients
    print(f"\nРецепт '{new_recipe}' успешно добавлен!")

def calculate_recipe_cost():
    recipe_name = input("\nВведите название рецепта для расчета стоимости: ").strip().lower()

    found_recipe = None
    for recipe in recipes:
        if recipe.lower() == recipe_name:
            found_recipe = recipe
            break

    if found_recipe is None:
        print("Рецепт не найден!")
        return

    ingredients = recipes[found_recipe]
    total_cost = 0

    print(f"\nИнгредиенты для рецепта '{found_recipe}':")
    for ingredient in ingredients:
        ingredient_index = np.where(ingredients_list == ingredient)[0]
        if len(ingredient_index) > 0:
            price = prices_list[ingredient_index[0]]
            total_cost += price
            print(f"  - {ingredient}: {price} тенге")
        else:
            print(f"  - {ingredient}: Цена не найдена")

    print(f"\nОбщая стоимость рецепта '{found_recipe}': {total_cost} тенге")

    if total_cost > 30000:
        discount = total_cost * 0.10
        total_cost -= discount
        print(f"Применена скидка 10%. Итоговая стоимость: {total_cost} тенге")
    else:
        print(f"Без скидки. Итоговая стоимость: {total_cost} тенге")

def main():
    while True:
        print("\nЧто вы хотите сделать?")
        print("1. Показать доступные рецепты и их стоимость")
        print("2. Добавить новый рецепт")
        print("3. Рассчитать стоимость рецепта")
        print("4. Выход")

        choice = input("Введите номер действия: ").strip()

        if choice == '1':
            print_recipes_and_prices()
        elif choice == '2':
            add_new_recipe()
        elif choice == '3':
            calculate_recipe_cost()
        elif choice == '4':
            print("До свидания!")
            break
        else:
            print("Неверный выбор, пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()
