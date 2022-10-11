from decimal import Decimal

from django import forms


class MoneyField(forms.DecimalField):

    def to_python(self, value):
        try:
            value = value.replace(' ', '').replace(',', '.')
            return super(MoneyField, self).to_python(value)
        except AttributeError:
            return Decimal(0)
