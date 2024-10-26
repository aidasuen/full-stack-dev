const readline = require('readline');

// Создаем интерфейс для чтения ввода
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// Функция для получения ввода
const askQuestion = (question) => {
    return new Promise((resolve) => {
        rl.question(question, (answer) => {
            resolve(answer);
        });
    });
};

// Основная логика
const main = async () => {
    // Четное или нечетное
    let inputNumber = await askQuestion("Введите число: ");
    let number = parseInt(inputNumber);
    let result = number % 2 === 0 ? "четное" : "нечетное";
    console.log(`${number} - ${result} число.`);

    // Фаренгейты
    let celsiusInput = await askQuestion('Введите температуру по Цельсию: ');
    let celsius = parseFloat(celsiusInput);

    if (isNaN(celsius)) {
        console.log("Ошибка: Не числовое значение");
    } else {
        let fahrenheit = (9 / 5) * celsius + 32;
        console.log(`${celsius} °C равно ${fahrenheit.toFixed(2)} °F`);
    }

    // Угадай число
    let numberToGuess = Math.floor(Math.random() * 10) + 1; // Случайное число от 1 до 10
    let attempts = 0;

    console.log("Загадала число от 1 до 10. Попробуй угадать:");

    while (true) {
        let guessInput = await askQuestion("Какие есть предположения? Введи число: ");
        let whoGuess = parseInt(guessInput);
        attempts++;

        if (whoGuess < numberToGuess) {
            console.log("Загаданное число больше.");
        } else if (whoGuess > numberToGuess) {
            console.log("Загаданное число меньше.");
        } else {
            console.log(`Поздравляю! Ты угадал число ${numberToGuess} за ${attempts} попыток.`);
            break;
        }
    }

    rl.close(); // Закрытие интерфейса
};

main(); // Запуск основной функции
