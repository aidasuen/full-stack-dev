import datetime

class Pricing:
    def __init__(self, original_price, customer_id, loyalty_customers):
        self.original_price = original_price  # Исходная цена товара
        self.customer_id = customer_id  # Идентификатор клиента
        self.loyalty_customers = loyalty_customers  # Список клиентов, участвующих в программе лояльности
        self.price = original_price  # Текущая цена после всех применённых операций

    def apply_basic_discount(self):
        """Применение базовой скидки (например, 5%)."""
        discount = 0.05  # 5% скидка
        discount_price = self.original_price * discount  # Базовая скидка от исходной цены
        self.price -= discount_price  # Применяем скидку к текущей цене
        print(f"После базовой скидки: {self.price:.2f}")

    def apply_loyalty_discount(self):
        """Применение скидки для участников программы лояльности (например, 5%)."""
        if self.customer_id in self.loyalty_customers:
            loyalty_discount = 0.05
            self.price -= self.price * loyalty_discount
            print(f"После скидки для лояльных клиентов: {self.price:.2f}")
        else:
            print("Нет скидки для лояльных клиентов, так как покупатель не является участником программы.")

    def apply_basic_tax(self):
        """Применение базового налога (например, 12%)."""
        tax = 0.12
        self.price += self.price * tax
        print(f"После базового налога: {self.price:.2f}")

    def apply_wildcard_tax(self):
        """Применение дополнительного налога (например, 4%), если минута чётная."""
        current_minute = datetime.datetime.now().minute
        if current_minute % 2 == 0:
            print("Дополнительный налог не применяется, так как минута чётная.")
        else:
            wildcard_tax = 0.04
            self.price += self.price * wildcard_tax
            print(f"После дополнительного налога: {self.price:.2f}")

    def calculate_final_price(self):
        """Рассчитывает и выводит итоговую цену."""
        print(f"Итоговая цена: {self.price:.2f}")
        return self.price


# Список ID клиентов, участвующих в программе лояльности
loyalty_customers = ["id100", "id101", "id102"]

# Получаем данные от пользователя
customer_id = input("Введите ваш ID клиента: ")
original_price = float(input("Введите цену товара: "))

# Создаем объект с введёнными данными
product = Pricing(original_price=original_price, customer_id=customer_id, loyalty_customers=loyalty_customers)

# Применяем все операции
product.apply_basic_discount()  # Применяем базовую скидку
product.apply_loyalty_discount()  # Применяем скидку для лояльных клиентов
product.apply_basic_tax()  # Применяем базовый налог
product.apply_wildcard_tax()  # Применяем дополнительный налог
final_price = product.calculate_final_price()  # Рассчитываем итоговую цену
