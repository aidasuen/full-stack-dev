def calculator():
    try:
        a = float(input("Введите число a: "))
        b = float(input("Введите число b: "))
        
        print("Выберите операцию:")
        print("1. Сложение")
        print("2. Вычитание")
        print("3. Умножение")
        print("4. Деление")

        operation = input("Введите номер операции (1/2/3/4): ")

        if operation == '1':
            result = a + b
            print(f"{a} + {b} = {result}")
        elif operation == '2':
            result = a - b
            print(f"{a} - {b} = {result}")
        elif operation == '3':
            result = a * b
            print(f"{a} * {b} = {result}")
        elif operation == '4':
            if b == 0:
                print("Ошибка: Деление на ноль невозможно.")
            else:
                result = a / b
                print(f"{a} / {b} = {result}")
        else:
            print("Ошибка: Неверный номер операции.")
    
    except ValueError:
        print("Ошибка: Пожалуйста, введите корректные числа.")

calculator()
