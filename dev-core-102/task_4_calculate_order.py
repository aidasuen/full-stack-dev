import datetime

# Функция для проверки номера участника программы лояльности
def is_loyalty_member(member_number):
    # Проверяем, что номер состоит только из цифр и имеет длину 4 символов
    return member_number.isdigit() and len(member_number) == 4

def calculate_total():
    # Запрашиваем у пользователя сумму заказа с проверкой корректности ввода
    while True:
        try:
            order_amount = float(input("Введите сумму заказа: "))
            if order_amount < 0:
                print("Сумма заказа не может быть отрицательной. Попробуйте снова.")
                continue
            break
        except ValueError:
            print("Введите корректное число для суммы заказа.")
    
    # Запрашиваем номер участника программы лояльности
    loyalty_member_number = input("Введите номер участника программы лояльности: ").strip()
    
    # Проверяем, является ли пользователь участником программы лояльности
    loyalty_program = is_loyalty_member(loyalty_member_number)
    
    # Запрашиваем код скидки
    discount_code = input("Введите код скидки (если есть): ").strip()
    
    # Изначальная скидка по программе лояльности
    discount = 0
    
    if loyalty_program:
        discount = 0.10  # 10% скидка для участников программы лояльности
    
    # Дополнительная скидка, если сумма заказа больше 1000
    if order_amount > 1000:
        discount += 0.05  # 5% скидка на сумму более 1000
    
    # Проверка скидки по коду
    if discount_code == "NEWYEAR2024":
        discount += 0.05  # 5% скидка по коду
    
    # Применяем скидку
    discounted_amount = order_amount * (1 - discount)
    
    # Получаем текущую минуту
    current_minute = datetime.datetime.now().minute
    
    # Налог 5% (применяется, если текущая минута не чётная)
    if current_minute % 2 != 0:
        tax = discounted_amount * 0.05
    else:
        tax = 0  # Налог не применяется, если минута чётная
    
    # Итоговая сумма
    total_amount = discounted_amount + tax
    
    # Выводим итоговую сумму
    print(f"Сумма заказа: {order_amount} тенге.")
    print(f"Применённая скидка: {discount * 100}%")
    print(f"Налог (если применим): {tax:.2f} тенге.")
    print(f"Итоговая сумма к оплате: {total_amount:.2f} тенге.")

# Запуск программы
calculate_total()
