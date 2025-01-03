def choose_trip():
    # Запрашиваем предпочтения пользователя
    vacation_type = input("Какой отдых вы предпочитаете: активный или расслабляющий? ").lower().strip()

    print(f"Вы ввели: '{vacation_type}'")

    # Если пользователь выбирает активный отдых
    if vacation_type == "активный":
        print("Для активного отдыха мы можем предложить следующие места:")
        print("1. Поход в горы")
        print("2. Конная прогулка")
        print("3. Катание на лыжах")
        place_choice = input("Выберите место для активного отдыха (введите номер): ").strip()

        # Сообщение в зависимости от выбора
        if place_choice == "1":
            print("Вы выбрали отдых в горах. Не забудьте взять с собой походную обувь и теплую одежду!")
        elif place_choice == "2":
            print("Вы выбрали конную прогулку. Возьмите с собой удобную одежду и обязательно запаситесь солнцезащитным кремом!")
        elif place_choice == "3":
            print("Вы выбрали катание на лыжах. Не забудьте лыжи, теплую одежду и защитные очки!")
        else:
            print("Вы выбрали неизвестный вариант. Пожалуйста, выберите один из предложенных вариантов.")

    # Если пользователь выбирает расслабляющий отдых
    elif vacation_type == "расслабляющий":
        print("Для расслабляющего отдыха мы можем предложить следующие места:")
        print("1. Пляж")
        print("2. SPA")
        print("3. Гостиница")
        place_choice = input("Выберите место для расслабляющего отдыха (введите номер): ").strip()

        # Сообщение в зависимости от выбора
        if place_choice == "1":
            print("Вы выбрали отдых на пляже. Не забудьте взять солнцезащитный крем!")
        elif place_choice == "2":
            print("Вы выбрали SPA. Пора побаловать себя и расслабиться!")
        elif place_choice == "3":
            print("Вы выбрали отдых в гостинице. Идеально для спокойного отдыха и комфортного времяпрепровождения!")
        else:
            print("Вы выбрали неизвестный вариант. Пожалуйста, выберите один из предложенных вариантов.")

    else:
        print("Пожалуйста, выберите между активным или расслабляющим отдыхом.")
        return

    # Запрашиваем бюджет
    try:
        budget = float(input("Введите ваш бюджет на поездку: "))
    except ValueError:
        print("Пожалуйста, введите корректное число для бюджета.")
        return

    # Рекомендации по месту отдыха в зависимости от бюджета
    if budget < 10000:
        print("ВЫ не можете ничего выбрать. Пожалуйста накопите побольше денег.")
    elif 10000 <= budget < 50000:
        print("С таким бюджетом вы можете выбрать отдых в SPA или любой вид активного отдыха.")
    elif 50000 <= budget < 200000:
        print("С таким бюджетом вы можете выбрать любой активный отдых, кроме отдыха на пляже.")
    elif 200000 <= budget <= 500000:
        print("С таким бюджетом открываются все варианты: поход в горы, катание на лыжах, конная прогулка, пляж или SPA.")
    else:
        print("С таким бюджетом вы можете позволить себе самые эксклюзивные варианты отдыха, включая курорты премиум-класса.")

    print("Желаем удачной поездки и отличного отдыха!")

# Запуск программы
choose_trip()
