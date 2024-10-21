function makesandwich() { 
let bread = "хлеб";
let filling = "сливочное масло"; 
let equipment = "холодильник"; 
let filling1 = "колбасу";
let filling2 = "сыр";
let equipment1 ="хлебницу";
let equipment2 ="столещницу"
let equipment3 = "доске"
// 1. Открываем холодильник
 console.log(`Открываем  ${equipment}`);
 // 2. Находим сливочное масло
console.log(`Находим  ${filling}`);
// 3. Находим колбасу
console.log(`Находим  ${filling1}`);
// 4. Находим сыр
console.log(`Находим  ${filling2}` );
// 5. Достаем колбасу
console.log(`Достаем ${filling1}`);
// 6. Достаем сыр
console.log(`Достаем  ${filling2}`);
// 7. Достаем сливочное масло
console.log(`Достаем  ${filling}`);
// 8. Кладем на столешницу колбасу, сыр и сливочное масло
console.log(`Кладем на  ${equipment2} ${filling1}, ${filling2} и ${filling}`);
// 9.Закрываем холодильник
console.log(`Закрываем ${equipment}`);
// 10. Открываем хлебницу
console.log(`Открываем ${equipment1}`);
// 11. Достаем хлеб
console.log(`Достаем ${bread}`);
// 12. Берем сливочное масло
console.log(`Берем ${filling}`); 
// 13. Намазываем сливочное масло на хлеб
console.log(`Намазываем ${filling} на ${bread}`); 
// 14. Берем колбасу 
console.log(`Берем ${filling1}`);
// 15. На доске разрезаем колбасу на слайсы
console.log(`Разрезаем на ${equipment3} ${filling1} на слайсы`);
// 16. Берем сыр
console.log(`Берем ${filling2}`);
// 17. Разрезаем сыр на слайсы
console.log(`Разрезаем ${filling2} на слайсы`);
// 18. Кладем сыр и колбасу на хлеб
console.log(`Кладем ${filling2} и ${filling1} на ${bread}`);
// 19. Кушаем
console.log("Кушаем");  
}
makesandwich()
