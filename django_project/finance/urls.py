from django.urls import path, reverse_lazy

from .views import (
    CategoriesListView,
    UserTransactionListView,
    TransactionCreateView,
    TransactionDetailView,
    TransactionUpdateView,
    TransactionDeleteView,
    FinanceFilterCreateView,
)


from . import views

urlpatterns = [
    path('finance/categories/', CategoriesListView.as_view(), name='finance-categories'),
    path('finance/transactions/', UserTransactionListView.as_view(), name='finance-transactions'),
    path('transaction/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('finance_filter/',
         FinanceFilterCreateView.as_view(success_url=reverse_lazy('finance-transactions')),
         name='finance-filter'),
    path('transaction/<int:pk>/update/',
         TransactionUpdateView.as_view(), name='transaction-update'),
    path('transaction/<int:pk>/delete/',
         TransactionDeleteView.as_view(success_url=reverse_lazy('finance-transactions')),
         name='transaction-delete'),
    path('finance/transactions/new/',
         TransactionCreateView.as_view(success_url=reverse_lazy('finance-transactions')),
         name='finance-new-transaction'),

]
