from django.urls import path
from . import views

urlpatterns = [
 
    path('login/', views.login_view, name='login'),
    path('', views.add_problem, name='help_list'),
    path('all_problem/', views.all_problems, name='all_problem' ),
    path('logout/', views.logout_user, name='logout'),
    path('thankyou/', views.thankyou, name='thankyou'),
    path('more/<int:problem_id>/', views.more_details, name='more'),
]
