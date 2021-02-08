import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.records = []
        # Дневной лимит
        self.limit = limit
        self.date_format = '%d.%m.%Y'

    def add_record(self, record):
        """Новая запись"""
        # record.date = isinstance(record.date, str) and dt.datetime.strptime(record.date, self.date_format) or record.date
        record.amount = isinstance(record.amount, str) and float(record.amount) or record.amount
        self.records.append(record)

    def get_today_stats(self):
        """Статистика за день"""
        return sum([rec.amount for rec in self.records if rec.date.date() == dt.date.today()])

    def get_week_stats(self):
        """Статистика за неделю"""
        return sum(
            [rec.amount for rec in self.records if rec.date.date() >= (dt.date.today() - dt.timedelta(days=7))])


class Record:
    def __init__(self, amount, comment, date=dt.datetime.now()):
        # Денежная сумма или количество килокалорий
        self.amount = amount
        # Поясняющий комментарий
        self.comment = comment
        # Дата создания записи
        date_format = '%d.%m.%Y'
        self.date = date != '' and (isinstance(date, str) and dt.datetime.strptime(date, date_format) or date) or date.date()


class CashCalculator(Calculator):
    """Калькулятор для подсчёта денег"""
    USD_RATE = 74.30
    EURO_RATE = 89.59
    currency = 'rub'
    balance = 0

    currency_translate = {
        "usd": "$",
        "euro": u"\u20AC",
        "rub": "руб."
    }

    def get_rates(self):
        if self.currency == 'usd':
            rates = self.balance / self.USD_RATE
        elif self.currency == 'euro':
            rates = self.balance / self.EURO_RATE
        else:
            return f'{self.balance} {self.currency_translate[self.currency]}'

        return f'{self.currency_translate[self.currency]}{"%.2f" % rates}'

    def get_balance(self):
        self.balance = self.limit - self.get_today_stats()
        return f'{self.get_rates()}'

    def get_today_cash_remained(self, currency):
        """Сколько денег можно потратить сегодня в рублях, долларах или евро"""
        self.currency = currency

        if self.get_today_stats() < self.limit:
            print(f'На сегодня осталось {self.get_balance()}')
        elif self.get_today_stats() > self.limit:
            print(f'Денег нет, держись: твой долг - {self.get_balance()}')
        else:
            print(f'Денег нет, держись {self.get_balance()}')


class CaloriesCalculator(Calculator):
    """Калькулятор для подсчёта калорий"""

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
cash_calculator.add_record(Record(amount=300, comment='бар в Танин др', date='04.02.2021'))
cash_calculator.add_record(Record(amount=150, comment='кабак в Риге', date='07.01.2021'))

print(cash_calculator.get_today_cash_remained('usd'))
# должно напечататься
# На сегодня осталось 555 руб

# Денег потрачено сегодня
print(f'Расход за сегодня: {cash_calculator.get_today_stats()}')
# Денег потрачено за неделю
print(f'Расход за семь дней: {cash_calculator.get_week_stats()}')
