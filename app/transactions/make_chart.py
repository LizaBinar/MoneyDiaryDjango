import calendar
import datetime
from datetime import timedelta

from django.db.models import Sum


def date_day_range(d1, d2):
    result = (d1 + timedelta(days=i) for i in range((d2 - d1).days + 1))
    return list(result)


def make_chart(transactions, grouping_by_date):
    result = {}
    label = []
    expenditure_data = []
    income_data = []
    for_income_charts = transactions.filter(transactions_type__main_type=True,
                                            data_time__month=datetime.date.today().month).values(
        grouping_by_date).annotate(
        Sum('money_value'))
    for_expenditure_charts = transactions.filter(transactions_type__main_type=False,
                                                 data_time__month=datetime.date.today().month).values(
        grouping_by_date).annotate(
        Sum('money_value'))

    income_date = []
    expenditure_date = []
    for transaction in for_income_charts:
        # label.append(transaction[grouping_by_date].day)
        income_date.append(transaction[grouping_by_date].day)
        income_data.append(float(transaction['money_value__sum']))
    for transaction in for_expenditure_charts:
        # if transaction[grouping_by_date.day] not in label:
        # label.append(transaction[grouping_by_date ].day)
        expenditure_date.append(transaction[grouping_by_date].day)
        expenditure_data.append(-(float(transaction['money_value__sum'])))

    # label.sort()

    # num_days = calendar.monthrange(datetime.date.today().year, datetime.date.today().month)[1]
    # days = [datetime.date(datetime.date.today().year, datetime.date.today().month, day) for day in range(1, num_days + 1)]

    cl = calendar.Calendar(firstweekday=0)
    days_generator = cl.itermonthdays(year=datetime.date.today().year, month=datetime.date.today().month)

    for day in days_generator:
        if day != 0:
            label.append(day)
    if not (income_date == [] and expenditure_date == []):
        data_count = 0
        for date in list(range(1, max(income_date + expenditure_date) + 1)):
            if date not in income_date:
                income_data.insert(data_count, 0)
            if date not in expenditure_date:
                expenditure_data.insert(data_count, 0)
            # label['data_count'] = date
            data_count += 1
        result['income_data'] = income_data
        result['expenditure_data'] = expenditure_data
    else:
        result['income_data'] = []
        result['expenditure_data'] = []
    result['label'] = list(label)
    return result
