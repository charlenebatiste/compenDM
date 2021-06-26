from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name="login"),
    path('user/<username>/', views.profile, name='profile'),
    path('logout/', views.logout_view, name="logout"),
    path('journals/create/', views.JournalCreate.as_view(), name='journals_create'),
    path('journals/<int:pk>/update/', views.JournalUpdate.as_view(), name='journals_update'),
    path('journals/<int:pk>/delete/', views.JournalDelete.as_view(), name='journals_delete'),
    path('journals/<int:journal_id>/', views.journals_show, name='journals_show'),
]