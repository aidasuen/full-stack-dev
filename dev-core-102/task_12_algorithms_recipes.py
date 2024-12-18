
recipes = {
    "Борщ": 4000,
    "Плов": 5000,
    "Салат оливье": 3000,
    "Пельмени": 4000,
    "Блины": 2000,
    "Суп-пюре из тыквы": 1500,
    "Котлеты": 2500,
    "Шашлык": 4500,
    "Сэндвич": 1000,
}

def bubble_sort(recipes):
    recipe_list = list(recipes.items()) 
    n = len(recipe_list)
    for i in range(n):
        for j in range(0, n-i-1):
            if recipe_list[j][1] > recipe_list[j+1][1]: 
                recipe_list[j], recipe_list[j+1] = recipe_list[j+1], recipe_list[j]
    return recipe_list

def binary_search(sorted_recipes, target_price):
    low, high = 0, len(sorted_recipes) - 1
    while low <= high:
        mid = (low + high) // 2
        if sorted_recipes[mid][1] == target_price:
            return sorted_recipes[mid][0]
        elif sorted_recipes[mid][1] < target_price:
            low = mid + 1
        else:
            high = mid - 1
    return None 

def greedy_algorithm(recipes, budget):
    sorted_recipes = bubble_sort(recipes)
    selected_recipes = []
    total_cost = 0
    for recipe, price in sorted_recipes:
        if total_cost + price <= budget:
            selected_recipes.append(recipe)
            total_cost += price
    return selected_recipes, total_cost

def main():
    budget = int(input("Введите свой бюджет (тенге): "))
    
    sorted_recipes = bubble_sort(recipes)
    print("Рецепты, отсортированные по стоимости:", [recipe[0] for recipe in sorted_recipes])

    target_price = int(input("Введите цену рецепта для поиска: "))
    recipe_found = binary_search(sorted_recipes, target_price)
    if recipe_found:
        print(f"Рецепт с такой ценой: {recipe_found}")
    else:
        print("Рецепт с такой ценой не найден.")
    
    selected_recipes, total_cost = greedy_algorithm(recipes, budget)
    print(f"Рецепты, которые можно приготовить за {budget} тенге: {selected_recipes}")
    print(f"Общая стоимость выбранных рецептов: {total_cost} тенге")

if __name__ == "__main__":
    main()