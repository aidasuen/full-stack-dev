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

