from django.urls import path
from pages import views


urlpatterns = [
    path("", views.landingpage, name='landingpage'),
    path('home/', views.home, name='home'),
    path('main/', views.main, name='main'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'), 
    path('flashcard/', views.flashcard, name='flashcard'),
    path('createflashcard/<str:flashcard_title>/', views.createflashcard, name='createflashcard'),
    path('displayflashcard/', views.displayflashcard, name='displayflashcard'),
    path('edit_flashcard/<str:flashcard_id>/', views.edit_flashcard, name='edit_flashcard'),
    path('delete_flashcard/<str:flashcard_id>/', views.delete_flashcard, name='delete_flashcard'),
    
    #NOTES FEATURE
    path('notes/', views.notes, name='note'),
    path('add_note', views.createnote, name='createnote'),
    path('display_note', views.displaynote, name='displaynote'),
    path('edit_note/<str:title>/', views.editnote, name='editnote'),
    path('quiz/', views.quiz, name = 'quiz'),
    path('takequiz', views.takequiz, name = 'takequiz'),
    path('creategroup', views.creategroup, name='creategroup'),
    path('group/<int:group_id>/', views.group, name='group'),
    path('addgroup', views.addgroup, name = 'addgroup'),
    path('shareflashcard/<int:group_id>/', views.shareflashcard, name='shareflashcard'),
    path('compiler/', views.compiler, name='compiler'),
    path('sharenote/<int:group_id>/', views.sharenote, name='sharenote'),
]