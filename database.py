#  Файл в котором находится интерфейс для работы с БД
# Всё что относится к БД тут
import sqlite3


class Database:
    def __init__(self, db_name: str, path=''):
        """
        Забираем базу из указанного места, если она лежит в корневой папке, то нужно лишь её название.
        """
        self.name = path + db_name
        self.db = sqlite3.connect(self.name)
        self.cur = self.db.cursor()

    def insert(self, tab_name: str, fields: tuple, values: tuple):
        """
         Функция что бы добавить новый объект в базу.
        :param tab_name: название таблицы
        :param fields: названия полей, в которые вставляем значения
        :param values: сами значения
        """

        self.cur.execute(f'INSERT INTO {tab_name}{fields} VALUES{values}')

    def new_table(self, tab_name: str, *keys: str):
        """
        Функция по созданию новой таблицы в базе. На вход подаётся её название, ключи в формате '(ключ + свойства)'
        Например мы хотим добавить таблицу с игроками. Тогда мы пишем так:
        new_table('players', 'id INTEGER PRIMARY KEY', 'name TEXT NOT NULL')
        :param tab_name: название таблицы
        :param keys: названия колонок
        """
        vals = ', '.join(keys)
        self.cur.execute(f'CREATE TABLE IF NOT EXISTS {tab_name} ({vals})')

    def get_val(self, tab_name: str, column: str, condition: str):
        """
        Получаем значения из таблицы по заданным условиям. Сомневаюсь, что будем ей пользоваться т.к. условия, как
        правило, слишком сложные что бы запихнуть их в 1 строку.
        :param tab_name: название таблицы
        :param column: колонка, из которой забираем значение
        :param condition: условие, при котором забираем значение
        :return: кортеж с данными(вроде как)
        """
        if not condition:
            return self.cur.execute(f'SELECT {column} from {tab_name}').fetchall()
        else:
            return self.cur.execute(f'SELECT {column} from {tab_name}'
                                    f'WHERE {condition}').fetchall()


# # Пример. Создаём базу с парочкой игроков.
# Players = Database('players.sqlite')
# Players.new_table('scores', 'id INTEGER PRIMARY KEY', 'name TEXT NOT NULL', 'score INTEGER')
# Players.insert('scores', ('id', 'name', 'score'), ('1', 'Steve', '2000'))
# Players.insert('scores', ('id', 'name', 'score'), ('2', 'Alex', '1500'))
# Players.insert('scores', ('id', 'name', 'score'), ('3', 'Eva', '1700'))
# Players.db.commit()
# Players.db.close()
