import datetime as dt


class Calculator:

    def __init__(self, limit):
        self.records = []
        self.limit: int = limit
        self.__today = dt.date.today()

    def add_record(self, record: 'Record'):
        """Новая запись."""
        self.records.append(record)

    def get_today_stats(self):
        """Статистика за день."""
        return sum([rec.amount if rec.date == self.__today
                    else 0 for rec in self.records])

    def get_week_stats(self):
        """Статистика за последние 7 дней."""
        all_spent = []
        week_ago = (self.__today - dt.timedelta(days=6))
        for rec in self.records:
            if rec.date >= week_ago and (rec.date <= self.__today):
                all_spent.append(rec.amount)

        return sum(all_spent)


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount: float = amount
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
        self.balance = self.limit - self.get_today_stats()
        if self.balance < 0:
            self.balance = self.get_today_stats() - self.limit
        rate, currency = self.currency_translate[self.currency]
        balance = "%.2f" % (self.balance / rate)
        return f'{balance} {currency}'

    def get_today_cash_remained(self, currency: str) -> str:
        """Доступно для трат сегодня в рублях, долларах или евро."""
        self.currency = currency
        balance = self.get_rates()

        if self.get_today_stats() < self.limit:
            return f'На сегодня осталось {balance}'
        elif self.get_today_stats() > self.limit:
            return f'Денег нет, держись: твой долг - {balance}'
        return 'Денег нет, держись'


class CaloriesCalculator(Calculator):
    """Калькулятор для подсчёта калорий."""

    def get_calories_remained(self) -> str:
        """Сколько калорий можно/нужно получить сегодня."""
        state = self.limit - self.get_today_stats()
        txt = ['Сегодня можно съесть что-нибудь ещё, '
               'но с общей калорийностью не более', f'{state}', 'кКал']
        if self.get_today_stats() < self.limit:
            return ' '.join(txt)
        return 'Хватит есть!'
