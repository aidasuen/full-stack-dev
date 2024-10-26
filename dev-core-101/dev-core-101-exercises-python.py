#четное и нечетное

number = int(input("Введите число: "))
result = "четное" if number % 2 == 0 else "нечетное"
print(f"{number} - {result} число.")

#угадай число

import random

number_to_guess = random.randint(1, 10)
attempts = 0

print("Загадала число от 1 до 100. Попробуй угадать:")

while True:
    who_guess = input("Какие есть предположения? Введи число: ")

  
    who_guess = int(who_guess)
    attempts += 1

  
    if who_guess < number_to_guess:
        print("Загаданное число больше.")
    elif who_guess > number_to_guess:
        print("Загаданное число меньше.")
    else:
        print(f"Поздравляю! ТЫ угадал число {number_to_guess} за {attempts} попыток.")
        break

#с Цельсия в Фаренгейт
def temp(celsius):
    # Преобразование Цельсия в Фаренгейт
    tf = (9 / 5) * celsius + 32
    return tf
try:
   
    celsius_input = float(input('Введите температуру по Цельсию: '))

  
    fahrenheit = temp(celsius_input)

    print(f"{celsius_input} °C равно {fahrenheit:.2f} °F")
    
except ValueError:
    print("Ошибка: пожалуйста, введите числовое значение.")
