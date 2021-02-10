import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.records = []
        self.limit: int = limit

    def add_record(self, record: 'Record'):
        """Новая запись."""
        self.records.append(record)

    def get_today_stats(self) -> int:
        """Статистика за день."""
        return sum([rec.amount if rec.date == dt.date.today()
                    else 0 for rec in self.records])

    def get_week_stats(self) -> int:
        """Статистика за последние 7 дней."""
        all_spent = []
        week_ago = (dt.date.today() - dt.timedelta(days=6))
        for rec in self.records:
            if rec.date >= week_ago and (rec.date <= dt.date.today()):
                all_spent.append(rec.amount)

        return sum(all_spent)


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount: int = amount
        self.comment: str = comment
        if date is None:
            self.date = (dt.datetime.now()).date()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class CashCalculator(Calculator):
    """Калькулятор для подсчёта денег."""
    USD_RATE = 60.00
    EURO_RATE = 70.00
    RUB_RATE = 1
    currency = 'rub'
    balance = 0

    currency_translate = {
        "usd": (USD_RATE, 'USD'),
        "eur": (EURO_RATE, 'Euro'),
        "rub": (RUB_RATE, 'руб')
    }

    def get_rates(self) -> str:
        """Курс валюты."""
        rate, name = self.currency_translate[self.currency]
        return f'{"%.2f" % (self.balance / rate)} {name}'

    def get_today_cash_remained(self, currency: str) -> str:
        """Сколько денег можно потратить сегодня в рублях, долларах или евро."""
        self.currency = currency
        self.balance = self.limit - self.get_today_stats()

        if self.get_today_stats() < self.limit:
            return f'На сегодня осталось {self.get_rates()}'
        elif self.get_today_stats() > self.limit:
            self.balance = self.get_today_stats() - self.limit
            return f'Денег нет, держись: твой долг - {self.get_rates()}'
        return 'Денег нет, держись'


class CaloriesCalculator(Calculator):
    """Калькулятор для подсчёта калорий."""

    def get_calories_remained(self) -> str:
        """Сколько калорий можно/нужно получить сегодня."""
        state = self.limit - self.get_today_stats()
        txt = 'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более'
        if self.get_today_stats() < self.limit:
            return f'{txt} {state} кКал'
        return 'Хватит есть!'
