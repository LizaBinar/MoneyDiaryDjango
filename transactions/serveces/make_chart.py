import calendar
import datetime

from django.db.models import Sum


# def date_day_range(d1, d2):
#     result = (d1 + timedelta(days=i) for i in range((d2 - d1).days + 1))
#     return list(result)


class ChartsLogic:

    def __init__(self):
        self.result = {}
        self.label = []
        self.expenditure_data = []
        self.income_data = []
        self.days_expenditure = []
        self.days_income = []

    def grouping_transactions(self, transactions, grouping_by_date, main_type):
        return transactions.filter(transactions_type__main_type=main_type,
                                   data_time__month=datetime.date.today().month).values(
            grouping_by_date).annotate(
            Sum('money_value'))

    def split_transactions_money_value(self, transactions, grouping_by_date):
        for_income_charts = self.grouping_transactions(transactions=transactions, grouping_by_date=grouping_by_date, main_type=True)
        for_expenditure_charts = self.grouping_transactions(transactions=transactions, grouping_by_date=grouping_by_date, main_type=False)
        return {'income_money_values': for_income_charts, 'expenditure_money_values': for_expenditure_charts}

    def split_money_value_and_days(self, income_money_values, expenditure_money_values, grouping_by_date):
        for transaction in income_money_values:
            self.days_income.append(transaction[grouping_by_date].day)
            self.income_data.append(float(transaction['money_value__sum']))
        for transaction in expenditure_money_values:
            self.days_expenditure.append(transaction[grouping_by_date].day)
            self.expenditure_data.append(-(float(transaction['money_value__sum'])))

    def generator_list_days_now_month(self):
        cl = calendar.Calendar(firstweekday=0)
        return cl.itermonthdays(year=datetime.date.today().year, month=datetime.date.today().month)

    def generator_list_labels(self, days_of_the_month):
        for day in days_of_the_month:
            if day != 0:
                self.label.append(day)

    def add_zeros_in_money_value(self):
        data_count = 0
        for date in list(range(1, max(self.days_income + self.days_expenditure) + 1)):
            if date not in self.days_income:
                self.income_data.insert(data_count, 0)
            if date not in self.days_expenditure:
                self.expenditure_data.insert(data_count, 0)
            data_count += 1

    def make_chart(self, transactions, grouping_by_date):

        money_values = self.split_transactions_money_value(transactions, grouping_by_date)
        income_money_values = money_values['income_money_values']
        expenditure_money_values = money_values['expenditure_money_values']

        self.split_money_value_and_days(income_money_values, expenditure_money_values, grouping_by_date)

        days_of_the_month = self.generator_list_days_now_month()

        self.generator_list_labels(days_of_the_month)

        if not (self.days_income == [] and self.days_expenditure == []):
            self.add_zeros_in_money_value()
            self.result['income_data'] = self.income_data
            self.result['expenditure_data'] = self.expenditure_data
        else:
            self.result['income_data'] = []
            self.result['expenditure_data'] = []
        self.result['label'] = list(self.label)
        return self.result
