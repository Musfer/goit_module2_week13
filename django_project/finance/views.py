from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Category, Transaction, Filter, FilterToCategories
# from .models import IncomeTransaction, OutcomeTransaction
from django.core.exceptions import ValidationError
import datetime
from django.utils import timezone
import zoneinfo
from .src import finance_plot


class CategoriesListView(ListView):  # new view
    model = Category
    template_name = 'finance/categories.html'  # <app>/<model>_<view_type>.html
    context_object_name = 'categories'


# class TransactionCreateView(LoginRequiredMixin, CreateView):
#     model = Transaction
#     fields = ['title', 'description', 'abs_balance_change', 'date', 'category']
#
#     def form_valid(self, form):
#         form.instance.owner = self.request.user
#         return super().form_valid(form)


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    fields = ['title', 'description', 'abs_balance_change', 'date', 'category']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class UserTransactionListView(LoginRequiredMixin, ListView):  # new view
    model = Transaction
    template_name = 'finance/transactions.html'  # <app>/<model>_<view_type>.html
    context_object_name = 'transactions'
    # paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if user:
            query = Transaction.objects.filter(owner=user).order_by('-date')
            user_filter = Filter.objects.filter(owner=user).order_by('-date_created').first()
            if user_filter is None:
                return query
            query = query.filter(date__range=[user_filter.start_date, user_filter.end_date]).order_by('-date')
            filter_to_category = FilterToCategories.objects.filter(filter=user_filter)
            category_ids = [x.category.id for x in filter_to_category]
            if category_ids:
                query = query.filter(category__in=category_ids)
            return query
        else:
            return None

    def get_context_data(self, **kwargs):
        transactions = self.get_queryset()
        income_data = {}
        outcome_data = {}
        for item in transactions:
            title = str(item.category)
            if len(title) > 5:
                title = title[:5]+"..."
            if str(item.category.type) == "+":
                if title not in income_data.keys():
                    income_data[title] = item.abs_balance_change
                else:
                    income_data[title] += item.abs_balance_change
            else:
                if title not in outcome_data.keys():
                    outcome_data[title] = item.abs_balance_change
                else:
                    outcome_data[title] += item.abs_balance_change
        chart_income = finance_plot.get_plot(income_data, title="Income")
        chart_outcome = finance_plot.get_plot(outcome_data, title="Outcome")
        chart_monthly = finance_plot.monthly_plot(transactions)

        context = super(ListView, self).get_context_data(**kwargs)

        context["chart_income"] = chart_income
        context["chart_outcome"] = chart_outcome
        context["monthly_chart"] = chart_monthly
        user = self.request.user
        kyiv_tz = zoneinfo.ZoneInfo("Europe/Kyiv")
        if user:
            user_filter = Filter.objects.filter(owner=user).order_by('-date_created').first()
            if user_filter is None:
                context['start_date'] = datetime.datetime(2020, 1, 1, 0, 0, tzinfo=kyiv_tz)
                context['end_date'] = timezone.now
                context['categories'] = "all"
                return context
            context['start_date'] = user_filter.start_date
            context['end_date'] = user_filter.end_date
            filter_to_category = FilterToCategories.objects.filter(filter=user_filter)
            context['categories'] = ", ".join([x.category.title for x in filter_to_category])
        return context


class TransactionDetailView(DetailView):
    model = Transaction
    # template_name = 'finance/transaction_detail.html'


class FilterDetailView(DetailView):
    model = Filter


class TransactionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Transaction
    fields = ['title', 'description', 'abs_balance_change', 'date', 'category']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        transaction = self.get_object()
        if self.request.user == transaction.owner:
            return True
        else:
            return False


class TransactionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Transaction
    success_url = '/'

    def test_func(self):
        transaction = self.get_object()
        if self.request.user == transaction.owner:
            return True
        else:
            return False


class FinanceFilterCreateView(LoginRequiredMixin, CreateView):
    model = Filter
    fields = ['start_date', 'end_date', 'categories']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
