from aiogram.types import ReplyKeyboardMarkup, \
                          KeyboardButton, \
                          ReplyKeyboardRemove
btnMarks = KeyboardButton("Узнать оценки")
btnChangeInfo = KeyboardButton("Изменить информацию")
reMarks = ReplyKeyboardMarkup(resize_keyboard=True).row(btnMarks, btnChangeInfo)
btnLearnType1 = KeyboardButton("Бакалавриат/Cпециалитет")
btnLearnType2 = KeyboardButton("Магистратура")
choiceLearnType = ReplyKeyboardMarkup(resize_keyboard=True).row(btnLearnType1, btnLearnType2)
btnChangeName = KeyboardButton("имя")
btnChangeSurname = KeyboardButton("фамилию")
btnChangeFathername = KeyboardButton("отчество")
btnChangeNZach = KeyboardButton("номер студенческого")
btnChangeLearnType = KeyboardButton("тип обучения")
btnChangeAll = KeyboardButton("все сразу")
btnBack = KeyboardButton("вернуться назад")
changeKeyboard = ReplyKeyboardMarkup(resize_keyboard=True).row(btnChangeName, btnChangeSurname,
                                                               btnChangeFathername).add().row(
                                                               btnChangeNZach,
                                                               btnChangeLearnType, btnChangeAll).add(
                                                               btnBack)
btnZero = ReplyKeyboardRemove()
