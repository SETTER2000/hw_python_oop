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
        return sum([rec.amount for rec in self.records
                    if rec.date == dt.date.today()])

    def get_week_stats(self):
        """Статистика за последние 7 дней"""
        all_spent = []

        for rec in self.records:
            if rec.date >= (dt.date.today() - dt.timedelta(days=6)) and \
                    (rec.date <= dt.date.today()):
                all_spent.append(rec.amount)

        return sum(all_spent)


class Record:
    def __init__(self, amount, comment, date=dt.datetime.now()):
        # Денежная сумма или количество килокалорий
        self.amount = amount
        # Поясняющий комментарий
        self.comment = comment
        # Дата создания записи
        if isinstance(date, str):
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        else:
            self.date = date.date()


class CashCalculator(Calculator):
    """Калькулятор для подсчёта денег"""
    USD_RATE = 74.30
    EURO_RATE = 89.59
    currency = 'rub'
    balance = 0

    currency_translate = {
        "usd": "USD",
        "eur": "Euro",
        "rub": "руб"
    }

    def get_rates(self):
        if self.currency == 'usd':
            rates = self.balance / self.USD_RATE
        elif self.currency == 'eur':
            rates = self.balance / self.EURO_RATE
        else:
            rates = self.balance

        return f'{"%.2f" % rates} {self.currency_translate[self.currency]}'

    def get_today_cash_remained(self, currency):
        """Сколько денег можно потратить сегодня в рублях, долларах или евро"""
        self.currency = currency
        self.balance = self.limit - self.get_today_stats()

        if self.get_today_stats() < self.limit:
            return f'На сегодня осталось {self.get_rates()}'
        elif self.get_today_stats() > self.limit:
            self.balance = self.get_today_stats() - self.limit
            return f'Денег нет, держись: твой долг - {self.get_rates()}'
        return 'Денег нет, держись'


class CaloriesCalculator(Calculator):
    """Калькулятор для подсчёта калорий"""

    def get_calories_remained(self):
        """Сколько калорий можно/нужно получить сегодня"""
        state = self.limit - self.get_today_stats()
        txt = 'Сегодня можно съесть что-нибудь ещё, ' \
              'но с общей калорийностью не более'
        if self.get_today_stats() < self.limit:
            return f'{txt} {state} кКал'
        return 'Хватит есть!'
