import unittest
from commands import main

tests = {
    "Дискрет. матем.(лекция) Новиков Ф.А. (Канал №1 ) 16:00": 'Канал: {} '.format(main.channels[0]),
    "Алгебра (пр.) 1,5 пары Афанасьева С.С. (Канал №3)": 'Канал: {} '.format(main.channels[2]),
    "Мат.анализ(лекция) 1.5пары Жуков И. Б. 09:30час. Канал №1": 'Канал: {} '.format(main.channels[0]),
    "Ин. Язык Рева О.Э. (Канал №2) а.422СЛК": 'Канал: {} '.format(main.channels[1])
}



class TestStringMethods(unittest.TestCase):
    def test_distant(self):
        self.assertEqual(list(tests.values()), [main.distant(key) for key in tests])
        self.assertEqual("", main.distant("Я люблю азербайджан"))



