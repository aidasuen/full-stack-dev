def get_positive_number(prompt):
    while True:
        try:
            number = float(input(prompt))
            if number < 0:
                print("Число должно быть положительным. Попробуйте снова.")
            else:
                return number
        except ValueError:
            print("Ошибка! Пожалуйста, введите число.")

def main():
    print("Программа для расчета стоимости заказа.")

    quantity = get_positive_number("Введите количество продуктов: ")
    
    if quantity == 0:
        print("Количество продуктов не может быть равно нулю.")
        return

    price = get_positive_number("Введите цену одного продукта: ")

    if price == 0:
        print("Цена продукта не может быть равна нулю.")
        return

    total_price = quantity * price
    print(f"Общая сумма заказа: {total_price:.2f} тенге.")

if __name__ == "__main__":
    main()
