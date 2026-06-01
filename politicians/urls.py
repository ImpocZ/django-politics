from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = 'politicians'

urlpatterns = [
    path('', views.parties_page, name='parties'),
    path('politicians/', views.politicians_page, name='politicians'),
    path('governments/', views.governments_page, name='governments'),
    path('government-officials/', views.government_officials_page, name='government_officials'),
    path('login/', views.SiteLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='politicians:parties'), name='logout'),
    path('register/', views.register_page, name='register'),
    path('parties/<int:pk>/edit/', views.PartyUpdateView.as_view(), name='party_edit'),
    path('politicians/<int:pk>/edit/', views.PoliticianUpdateView.as_view(), name='politician_edit'),
    path('governments/<int:pk>/edit/', views.GovernmentUpdateView.as_view(), name='government_edit'),
    path('government-officials/<int:pk>/edit/', views.GovernmentOfficialUpdateView.as_view(), name='government_official_edit'),
]
