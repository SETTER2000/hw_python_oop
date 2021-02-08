import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.records = []
        # Дневной лимит
        self.limit = limit

    def add_record(self, record):
        """Новая запись"""
        self.records.append(record)

    def get_today_stats(self):
        """Статистика за день"""
        pass

    def get_week_stats(self):
        """Статистика за неделю"""
        pass


class Record:
    def __init__(self, amount, comment, date=''):
        # Денежная сумма или количество килокалорий
        self.amount = amount
        # Поясняющий комментарий
        self.comment = comment
        # Дата создания записи
        self.date = date and date or dt.datetime.now()

    def get_date(self):
        print(self.date)


class CashCalculator(Calculator):
    """Калькулятор для подсчёта денег"""
    USD_RATE = 74.30
    EURO_RATE = 89.59

    def __init__(self, limit):
        super().__init__(limit)

    def get_today_cash_remained(self, currency):
        """Сколько денег можно потратить сегодня в рублях, долларах или евро"""

        expense = sum([record.amount for record in self.records])
        balance = "%.2f" % (self.limit - expense)
        currency = currency == 'rub' and 'руб.' or currency == 'usd' and 'долл.' or 'евро'

        if expense < self.limit:
            print(f'На сегодня осталось {balance} {currency}')
        elif expense > self.limit:
            print(f'Денег нет, держись: твой долг - {balance} {currency}')
        else:
            print(f'Денег нет, держись {balance} {currency}')


class CaloriesCalculator(Calculator):
    """Калькулятор для подсчёта калорий"""

    def __init__(self, limit):
        super().__init__(limit)

    def get_calories_remained(self):
        """Сколько калорий можно/нужно получить сегодня"""
        pass


# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(1000)


# дата в параметрах не указана,
# так что по умолчанию к записи
# должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=400.23, comment='кофе'))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=300, comment='бар в Танин др', date='08.11.2019'))


print(cash_calculator.get_today_cash_remained('euro'))
# должно напечататься
# На сегодня осталось 555 руб