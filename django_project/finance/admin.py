from django.contrib import admin

from .models import Category, Transaction, Filter, FilterToCategories  # ,  IncomeTransaction, OutcomeTransaction
# from .models import Income, Outcome

admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(Filter)
admin.site.register(FilterToCategories)
# admin.site.register(Outcome)
# admin.site.register(Income)
# admin.site.register(IncomeTransaction)
# admin.site.register(OutcomeTransaction)

