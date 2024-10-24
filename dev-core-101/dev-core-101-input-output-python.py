import datetime
name = input("Введите ваше имя: ")
age = int(input("Введите ваш возраст: "))
today= datetime.date.today()
year = (today.year- age)  + 100
print(f"Привет, {name}. Вам исполниться 100 лет в {year} лет.")