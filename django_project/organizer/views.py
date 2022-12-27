from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Note


# def home(request):  # old view
#     context = {
#         'notes': Note.objects.all()
#     }
#     return render(request, "organizer/home.html", context)


class NoteListView(ListView):  # new view
    model = Note
    template_name = 'organizer/home.html'  # <app>/<model>_<view_type>.html
    context_object_name = 'notes'
    ordering = ['-date_posted']
    paginate_by = 5


class UserNoteListView(ListView):  # new view
    model = Note
    template_name = 'organizer/user_notes.html'  # <app>/<model>_<view_type>.html
    context_object_name = 'notes'
    # ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Note.objects.filter(author=user).order_by('-date_posted')


class NoteDetailView(DetailView):
    model = Note


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Note
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        note = self.get_object()
        if self.request.user == note.author:
            return True
        else:
            return False


class NoteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Note
    success_url = '/'

    def test_func(self):
        note = self.get_object()
        if self.request.user == note.author:
            return True
        else:
            return False


def about(request):
    return render(request, "organizer/about.html", {'title': 'About'})

