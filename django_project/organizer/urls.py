from django.urls import path
from .views import (
    NoteListView,
    NoteDetailView,
    NoteCreateView,
    NoteUpdateView,
    NoteDeleteView,
    UserNoteListView,

)


from . import views

urlpatterns = [
    # path('', views.home, name='organizer-home'), #  old view
    # path('', NoteListView.as_view(), name='organizer-home'),
    path('', NoteListView.as_view(), name='organizer-home'),
    path('user/<str:username>', UserNoteListView.as_view(), name='user-notes'),
    path('note/<int:pk>/', NoteDetailView.as_view(), name='note-detail'),
    path('note/new/', NoteCreateView.as_view(), name='note-create'),
    path('note/<int:pk>/update/', NoteUpdateView.as_view(), name='note-update'),
    path('note/<int:pk>/delete/', NoteDeleteView.as_view(), name='note-delete'),
    path('about/', views.about, name='organizer-about'),

]
