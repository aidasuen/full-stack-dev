def get_product_data():
  
    products = []
    while True:
        user_input = input("Введите цену продукта или 'стоп' для завершения: ")
        if user_input.lower() == 'стоп':
            break
        try:
            price = float(user_input)
            products.append(price)
        except ValueError:
            print("Пожалуйста, введите корректное число.")
    return products

def apply_discount(price):
    return price * 0.9 if price > 100 else price

def main():
    print("Программа для расчета скидки на продукты.")
   
    products = get_product_data()
    
    discounted_products = list(filter(lambda x: x > 100, products))  # Продукты для скидки
    discounted_prices = list(map(apply_discount, discounted_products))  # Применение скидки

    total_without_discount = sum(products)
    total_with_discount = sum(discounted_prices) + sum(x for x in products if x <= 100)
    
    print(f"Общая сумма без скидки: {total_without_discount:.2f}")
    print(f"Общая сумма с учетом скидки: {total_with_discount:.2f}")
    
if __name__ == "__main__":
    main()
