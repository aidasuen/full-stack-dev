import requests
import numpy as np
import pandas as pd

def get_temperature(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"]
        return temperature
    else:
        print(f"Ошибка: статус код {response.status_code}")
        return None

API_KEY = "cb20080b341abc961a3858ba48b025c0"  # API-ключ
city = "Almaty"  
temperature = get_temperature(city, API_KEY)

if temperature is not None:
    print(f"Температура в городе {city}: {temperature}°C")
    np_temperature = np.array([temperature])
    print(f"Температура как NumPy массив: {np_temperature}")
    mean_temperature = np.mean(np_temperature)
    print(f"Средняя температура: {mean_temperature:.2f}°C")

    df = pd.DataFrame({
        'Город': [city],
        'Температура (°C)': [temperature],
        'Средняя температура (°C)': [mean_temperature]
    })
    
    # Выведем DataFrame
    print("\nДанные о температуре в формате DataFrame:")
    print(df)
else:
    print("Не удалось получить температуру.")



