from django.urls import path
from . import views
from .views import AnalysisCategoryChartDataView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.index, name='index'),
    path('<int:id>', views.view_journal, name='view_journal'),
    path('add/', views.add, name='add'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('dashboard', views.dashboard, name='orders_count'),
    path('journal/<int:journal_id>/report/', views.journal_report, name='journal_report'),
    #---------------------------------------------------------------
    path('price', views.index_price, name='price'),
    path('add_price/', views.add_price, name='add_price'),
    path('edit_price/<int:id>/', views.edit_price, name='edit_price'),
    path('delete_price/<int:id>/', views.delete_price, name='delete_price'),
    #---------------------------------------------------------------
    path('dashboard', AnalysisCategoryChartDataView.as_view(), name='analysis_category_chart_data'),
    #---------------------------------------------------------------
    path('chat/', views.home, name='home'),
    path('<str:room>/', views.room, name='room'),
    path('chat/checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    
]