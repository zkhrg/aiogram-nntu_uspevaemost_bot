from aiogram.dispatcher.filters.state import StatesGroup, State


class Marks(StatesGroup):
    name = State()
    surname = State()
    fathername = State()
    n_zach = State()
    learn_type = State()
    knowMarks = State()
    check = State()


class Changes(StatesGroup):
    st1 = State()
    chngName = State()
    chngSurname = State()
    chngFathername = State()
    chngNZach = State()
    chngLearnType = State()
