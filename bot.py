import logging
import config
import parse as par
import keyboard as kb
import queries as q
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode
from aiogram.dispatcher import FSMContext
from states import Marks, Changes
from aiogram.contrib.fsm_storage.memory import MemoryStorage


# logging
logging.basicConfig(level=logging.INFO)

# init
bot = Bot(token=config.API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(state="*", commands=['start'])
async def greetings(message: types.Message):
    await message.answer("Что хочешь сделать?", reply_markup=kb.reMarks)


@dp.message_handler(state="*", text='Узнать оценки')
async def choosing(message: types.Message, state: FSMContext):
    if q.checkChatId(message.chat.id):  # есть ли chat_id в базе
        r1 = q.findData(message.chat.id)
        if par.form_marks(r1, 1):
            q_sem = par.quantity_sem(r1)
            await bot.send_message(message.from_user.id, f"Введи номер семеcтра:\n(у тебя их {q_sem})",
                                   reply_markup=kb.btnZero)
            await Marks.knowMarks.set()
        else:
            await bot.send_message(message.from_user.id, "Студента с такими данными не найдено.\n"
                                                         f"Проверь, вот что ты ввел:\n"
                                                         f"{q.actualInfo(message.chat.id)}",
                                   reply_markup=kb.reMarks, parse_mode=ParseMode.HTML)
            await state.finish()
    else:
        await bot.send_message(message.from_user.id, "Для того чтобы начать, нужно указать свои данные, "
                                                     "начнем с имени:", reply_markup=kb.btnZero)
        q.addChatId(message.chat.id)
        await Marks.name.set()


@dp.message_handler(state=Marks.knowMarks)
async def knowMarks(message: types.Message, state: FSMContext):
    try:
        sem_n = int(message.text)
        r1 = q.findData(message.chat.id)
        if 0 < sem_n <= par.quantity_sem(r1):
            par.form_marks(r1, sem_n-1)
            await message.answer(par.form_marks(r1, sem_n - 1), reply_markup=kb.reMarks, parse_mode=ParseMode.HTML)
            await state.finish()
        else:
            await bot.send_message(message.from_user.id, "Неправильно введен семестр!", reply_markup=kb.reMarks)
            await state.finish()
    except Exception:
        await bot.send_message(message.from_user.id, "Нужна цифра/число, а не текст!", reply_markup=kb.reMarks)
        await state.finish()


@dp.message_handler(state="*", text='Изменить информацию')
async def changing(message: types.Message):
    if q.checkChatId(message.chat.id):  # есть ли chat_id в базе
        await bot.send_message(message.from_user.id, "Что нужно изменить?", reply_markup=kb.changeKeyboard)
        await Changes.st1.set()
    else:
        await bot.send_message(message.from_user.id, "Для того чтобы начать, нужно указать свои данные,"
                                                     "начнем с имени:", reply_markup=kb.btnZero)
        q.addChatId(message.chat.id)
        await Marks.name.set()


@dp.message_handler(state=Marks.name)
async def change_n_main(message: types.Message):
    name = message.text
    q.changeName(name, message.chat.id)
    await message.answer("Введи свою фамилию:")

    await Marks.next()


@dp.message_handler(state=Marks.surname)
async def change_sn_main(message: types.Message, state: FSMContext):
    surname = message.text
    q.changeSurname(surname, message.chat.id)
    await message.answer("Введи свое отчество:")

    await Marks.fathername.set()


@dp.message_handler(state=Marks.fathername)
async def change_fn_main(message: types.Message, state: FSMContext):
    fathername = message.text
    q.changeFathername(fathername, message.chat.id)
    await message.answer("Введи свой номер студенческого:")

    await Marks.next()


@dp.message_handler(state=Marks.n_zach)
async def change_nz_main(message: types.Message):
    n_zach = message.text
    q.changeNZach(n_zach, message.chat.id)
    await message.answer("Выбери свой тип обучения:", reply_markup=kb.choiceLearnType)

    await Marks.next()


@dp.message_handler(state=Marks.learn_type)
async def change_l_main(message: types.Message, state: FSMContext):
    learn_type = message.text
    if learn_type == 'Бакалавриат/Cпециалитет':
        q.changeLearnType('bak_spec', message.chat.id)
    else:
        q.changeLearnType('mag', message.chat.id)

    await message.answer("Что хочешь сделать?", reply_markup=kb.reMarks)
    await state.finish()


@dp.message_handler(text='имя', state=Changes.st1)
async def change_n1(message: types.Message):
    await message.answer("Введи имя:", reply_markup=kb.btnZero)

    await Changes.chngName.set()


@dp.message_handler(state=Changes.chngName)
async def change_n2(message: types.Message, state: FSMContext):
    name = message.text
    q.changeName(name, message.chat.id)
    await message.answer("Имя успешно изменено!", reply_markup=kb.reMarks)

    await state.finish()


@dp.message_handler(text='фамилию', state=Changes.st1)
async def change_sn1(message: types.Message):
    await message.answer("Введи фамилию:", reply_markup=kb.btnZero)

    await Changes.chngSurname.set()


@dp.message_handler(state=Changes.chngSurname)
async def change_sn2(message: types.Message, state: FSMContext):
    surname = message.text
    q.changeSurname(surname, message.chat.id)
    await message.answer("Фамилия успешно изменена!", reply_markup=kb.reMarks)

    await state.finish()


@dp.message_handler(text='отчество', state=Changes.st1)
async def change_sn1(message: types.Message):
    await message.answer("Введи отчество:", reply_markup=kb.btnZero)

    await Changes.chngFathername.set()


@dp.message_handler(state=Changes.chngFathername)
async def change_fn2(message: types.Message, state: FSMContext):
    fathername = message.text
    q.changeFathername(fathername, message.chat.id)
    await message.answer("Отчество успешно изменено!", reply_markup=kb.reMarks)

    await state.finish()


@dp.message_handler(text='номер студенческого', state=Changes.st1)
async def change_sn1(message: types.Message):
    await message.answer("Введи номер студенческого:", reply_markup=kb.btnZero)

    await Changes.chngNZach.set()


@dp.message_handler(state=Changes.chngNZach)
async def change_nz2(message: types.Message, state: FSMContext):
    n_zach = message.text
    q.changeNZach(n_zach, message.chat.id)
    await message.answer("Номер студенческого успешно изменен!", reply_markup=kb.reMarks)

    await state.finish()


@dp.message_handler(text='тип обучения', state=Changes.st1)
async def change_l1(message: types.Message):
    await message.answer("Выбери тип обучения:", reply_markup=kb.choiceLearnType)

    await Changes.chngLearnType.set()


@dp.message_handler(state=Changes.chngLearnType)
async def change_l2(message: types.Message, state: FSMContext):
    learn_type = message.text
    if learn_type == 'Бакалавриат/Cпециалитет':
        q.changeLearnType('bak_spec', message.chat.id)
    elif learn_type == 'Магистратура':
        q.changeLearnType('mag', message.chat.id)
    else:
        q.changeLearnType(learn_type, message.chat.id)

    await message.answer("Тип обучения успешно изменен!", reply_markup=kb.reMarks)

    await state.finish()


@dp.message_handler(text='все сразу', state=Changes.st1)
async def answer_name(message: types.Message):
    await message.answer("Начали. Вводи имя:", reply_markup=kb.btnZero)

    await Marks.name.set()


@dp.message_handler(text='вернуться назад', state=Changes.st1)
async def answer_name(message: types.Message, state: FSMContext):
    await message.answer("Что хочешь сделать?", reply_markup=kb.reMarks)

    await state.finish()


# запуск
if __name__ == '__main__':
    executor.start_polling(dp)
