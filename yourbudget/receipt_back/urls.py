from django.urls import path

from . import views, api

handler404 = 'receipt_back.views.not_found'

urlpatterns = [
    path('index', views.index, name='index'),
    path('alltrips', views.alltrips, name='alltrips'),
    path('login', views.LoginView.as_view(), name='login_view'),
    path('registration', views.RegistrationView.as_view(), name='registration_view'),
    path('logout', views.logout_view, name='logout_view'),
    path('current_data', api.get_current_data, name='current_data'),
    path('save_receipt', api.Telegram.save_receipt, name='save_receipt'),
    path('save_trip_manual', api.Telegram.save_trip_manual, name='save_trip_manual'),
    path('all_trips_data', api.get_all_trips_data, name='all_trips_data'),
    path('settings', views.SettingsView.as_view(), name='settings_view'),
    path('profile', views.ProfileView.as_view(), name='user_view')
]
