from django.contrib import admin
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Currency, AccountsType, Accounts, TransactionsType, Transactions, Icons


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title')


class IconsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'file', 'unicode', 'unicode_icons')
    list_display_links = ('id', 'title')
    list_editable = ('unicode', 'unicode_icons')


class AccountsTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title')


class TransactionsTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'main_type', 'category', 'icons', 'currency', 'owner')
    list_display_links = ('id', 'main_type', 'category')
    search_fields = ('id', 'main_type')
    list_editable = ('currency', 'owner', 'icons')
    list_filter = ('category', 'currency', 'owner')
    exclude = ('owner',)  # скрыть author поле, чтобы оно не отображалось в форме изменений

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.owner = request.user
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super(TransactionsTypeAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['currency'].queryset = Currency.objects.all()
        return form


class AccountsAdmin(admin.ModelAdmin):
    list_display = ('id', 'balans', 'title', 'owner', 'accounts_type', 'currency')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'owner')
    list_editable = ('owner', 'accounts_type')
    list_filter = ('owner', 'accounts_type', 'currency')
    exclude = ('owner',)  # скрыть author поле, чтобы оно не отображалось в форме изменений

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.owner = request.user 
        super().save_model(request, obj, form, change)


class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'money_value', 'comment', 'transactions_type', 'owner', 'data_time', 'accounts')
    list_display_links = ('id', 'money_value')
    search_fields = ('comment', 'owner')
    list_editable = ('transactions_type', 'owner')
    list_filter = ('transactions_type', 'owner')
    exclude = ('owner',)  # скрыть author поле, чтобы оно не отображалось в форме изменений

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.owner = request.user
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super(TransactionsAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['transactions_type'].queryset = TransactionsType.objects.filter(owner=request.user)
        form.base_fields['accounts'].queryset = Accounts.objects.filter(owner=request.user)
        return form

    """  
   @receiver(pre_save)
       def pre_save_handler(self, obj, *args, **kwargs):
           # some case
           if obj.currency_id != obj.accounts_id.currency_id:
               raise Exception('OMG')"""


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(AccountsType, AccountsTypeAdmin)
admin.site.register(Accounts, AccountsAdmin)
admin.site.register(TransactionsType, TransactionsTypeAdmin)
admin.site.register(Transactions, TransactionsAdmin)
admin.site.register(Icons, IconsAdmin)

'''
Todo.objects.filter(user=request.user)

staff_member = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    limit_choices_to={'is_staff': True},
)
'''
