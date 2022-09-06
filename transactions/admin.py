from django.contrib import admin

from .models import Currency, AccountsType, Accounts, TransactionsType, Transactions


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title')


class AccountsTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title')


class TransactionsTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'main_type', 'category', 'currency_id', 'owner_id')
    list_display_links = ('id', 'main_type', 'category')
    search_fields = ('id', 'main_type')
    list_editable = ('currency_id', 'owner_id')
    list_filter = ('category', 'currency_id', 'owner_id')
    exclude = ('owner_id',)  # скрыть author поле, чтобы оно не отображалось в форме изменений

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.owner_id = request.user
        super().save_model(request, obj, form, change)


class AccountsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner_id', 'accounts_type_id', 'currency_id')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'owner_id')
    list_editable = ('owner_id', 'accounts_type_id')
    list_filter = ('owner_id', 'accounts_type_id', 'currency_id')
    exclude = ('owner_id',)  # скрыть author поле, чтобы оно не отображалось в форме изменений

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.owner_id = request.user
        super().save_model(request, obj, form, change)


class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'money_value', 'comment', 'currency_id', 'transactions_type_id', 'owner_id', 'data_time')
    list_display_links = ('id', 'money_value')
    search_fields = ('data_time', 'comment', 'owner_id')
    list_editable = ('transactions_type_id', 'owner_id', 'currency_id')
    list_filter = ('transactions_type_id', 'owner_id', 'currency_id')
    exclude = ('owner_id',)  # скрыть author поле, чтобы оно не отображалось в форме изменений

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.owner_id = request.user
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super(TransactionsAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['transactions_type_id'].queryset = TransactionsType.objects.filter(owner_id=request.user)
        return form


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(AccountsType, AccountsTypeAdmin)
admin.site.register(Accounts, AccountsAdmin)
admin.site.register(TransactionsType, TransactionsTypeAdmin)
admin.site.register(Transactions, TransactionsAdmin)



'''
Todo.objects.filter(user=request.user)

staff_member = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    limit_choices_to={'is_staff': True},
    
)

'''
