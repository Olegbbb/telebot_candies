from create import dp 
from aiogram import types
from random import randint as ri


total_candy = 150
take_candy = 0
count = 150



@dp.message_handler(commands=['start'])
async def mes_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}. Вводи /game чтобы играть или /help для просмотра других команд')

@dp.message_handler(commands=['help'])
async def mes_help(message: types.Message):
    await message.answer(f'/game - Начало новой игры\n/set и число - выбор общего количества конфет\n/rules - Правила игры')


@dp.message_handler(commands=['set'])
async def mes_set(message: types.Message):
    global total_candy
    global count 
    count = int(message.text.split()[1])
    await message.answer(f'Количество конфет теперь: {count}')



@dp.message_handler(commands=['rules'])
async def mes_rules(message: types.Message):
    await message.answer('''На столе лежит определенное количество конфет. 
    Каждый ход состоит в том, что играющий берет со стола от 1 до 28 конфет.
      Тот, кто забирает со стола последнюю конфету, выигрывает партию.
      Нельзя не брать конфеты и брать больше 28''')
    

    
@dp.message_handler(commands=['game'])
async def mes_game(message: types.Message):
    global total_candy 
    global take_candy
    global count
    total_candy = count
    turn =  ri(0,1)
    if turn == 0:
        await message.answer(f'Жребий пал на тебя, на столе {total_candy} конфет, ходи ')
    else: 
        await message.answer('Жребий пал на бота')
        if total_candy % 29 != 0:
            take_candy = total_candy % 29
        else: 
            take_candy = ri(1,28)
            total_candy -= take_candy
        total_candy -= take_candy
        await message.answer(f'Бот взял {take_candy} конфет, на столе осталось {total_candy}')
        await message.answer('Ваш ход')

    
@dp.message_handler(text=list(map(str,(i for i in range(1,29)))))
async def player_turn(message: types.Message):
    global take_candy
    global total_candy
    take_candy = int(message.text)
    total_candy -= take_candy
    if total_candy > 0:
        await message.answer(f'Вы взяли {take_candy} конфет, осталось {total_candy}')
        if total_candy % 29 != 0:
                take_candy = total_candy % 29
        else: 
            take_candy = ri(1,28)
        total_candy -= take_candy
        await message.answer(f'Бот взял {take_candy} конфет, на столе осталось {total_candy}')
        if total_candy > 0:
            await message.answer('Ваш ход')
        else: 
            await message.answer('Победил бот! Чтобы начать заново введи /game')
    else: 
        await message.answer('Вы победили! Чтобы начать заново введи /game')



@dp.message_handler()
async def mes_all(message: types.Message):
    if message.text.isdigit():
        await message.answer('Введи целое число от 1 до 28')
    else:
        await message.answer(f'{message.from_user.full_name}, я не знаю что значит {message.text}')

