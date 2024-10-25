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
