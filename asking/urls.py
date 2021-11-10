from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('asking/', views.asking, name='asking'),
    path('asking_change/', views.asking_change, name='asking_create'),
    path('asking_change/<int:asking_id>', views.asking_change, name='asking_change'),
    path('question_change/<int:asking_id>_<int:question_id>', views.asking_change, name='asking_change'),
    path('asking_start/<int:asking_id>', views.start_question, name='start_question'),
    path('asking_go/<int:asking_id>_<int:question_id>', views.asking_go, name='question'),
    path('get_solved_askings/<int:user_id>', views.get_solved_askings, name='get_solved_askings'),
    path('get_solved_questions/<int:user_id>_<int:asking_id>', views.get_solved_questions, name='get_solved_questions'),
]
