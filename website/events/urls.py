from django.urls import path

from .views import *

urlpatterns = [
    path('', EventsView.as_view(), name='event_list'),
    path('filter/', FilterEventsView.as_view(), name='filter'),
    path('add-rating/', AddStarRating.as_view(), name='add_rating'),
    path('search/', Search.as_view(), name='search'),

    path('<slug:slug>/', EventDetailView.as_view(), name='event_detail'),
    path('review/<int:pk>/', AddReview.as_view(), name='add_review'),
    path('avtor/<str:slug>/', AvtorView.as_view(), name='avtor_detail'),

]