import unittest
import main
tests = {
    'distant' : ['Канал: {} '.format(main.channels[n]) for n in range(12)],
    'lesson' : [
"Дискрет. матем.(лекция) Новиков Ф.А. (Канал №1 ) 16:00"
    ]
}



class TestStringMethods(unittest.TestCase):
    def test_distant(self):
        self.assertEqual(main.distant(tests['lesson'][0]), tests['distant'][0])
