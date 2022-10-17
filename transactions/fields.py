from django import forms


class MoneyField(forms.DecimalField):

    def to_python(self, value):
        value = value.replace(' ', '').replace(',', '.')
        return super(MoneyField, self).to_python(value)