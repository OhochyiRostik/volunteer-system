from django.db.models import Q, Case, When
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from .recommender import get_recommendations
from .models import *
from .forms import ReviewForm, RatingForm


class GenreYear:
    def get_genres(self):
        return SubCategory.objects.all()

    def get_years(self):
        return Event.objects.filter(draft=False).values('year')


# class EventsView(GenreYear, ListView):
#     model = Event
#     queryset = Event.objects.filter(draft=False)
#     # template_name = 'events/event_list.html'
#     # def get(self, request):
#     #     events = event.objects.all()
#     #     return render(request, 'events/event_list.html', {'event_list': events})

class EventsView(ListView):
    model = Event
    queryset = Event.objects.filter(draft=False)
    # template_name = 'events/event_list.html'
    # context_object_name = 'event_list'

    def get_queryset(self):
        """
        Отримує список подій, відсортований за рекомендаціями.
        """
        # user_id = self.request.user.id
        user_id = 1  # ID адміністратора (або змініть на `self.request.user.id` за потреби)
        events = self.queryset
        print("----------")
        print(events)
        print("-----------")
        event_ids = list(events.values_list('id', flat=True))  # Список ID подій

        # Отримуємо відсортовані рекомендації
        recommended_ids = get_recommendations(user_id, event_ids)

        # Створюємо умови для сортування
        preserved_order = Case(*[
            When(id=event_id, then=pos) for pos, event_id in enumerate(recommended_ids)
        ])

        # Сортуємо події відповідно до збереженого порядку
        sorted_queryset = events.filter(id__in=recommended_ids).order_by(preserved_order)
        return sorted_queryset



class EventDetailView(GenreYear, DetailView):
    model = Event
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        return context
    # def get(self, request, slug):
    #     event = Event.objects.get(url=slug)
    #     return render(request, 'events/event_detail.html', {'event': event})


class AddReview(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        event = Event.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.event = event
            # form.event_id = pk
            form.save()
        return redirect(event.get_absolute_url())


class AvtorView(GenreYear, DetailView):
    model = Avtor
    template_name = 'events/avtor.html'
    slug_field = 'name'


class FilterEventsView(GenreYear, ListView):
    def get_queryset(self):
        if 'genre' in self.request.GET and 'year' in self.request.GET:
            queryset = Event.objects.filter(
                Q(year__in=self.request.GET.getlist("year")), Q(genres__in=self.request.GET.getlist("genre"))
            )
        else:
            queryset = Event.objects.filter(
                Q(year__in=self.request.GET.getlist("year")) | Q(genres__in=self.request.GET.getlist("genre"))
            )
        return queryset
    # def get_queryset(self):
    #     queryset = Event.objects.filter(Q(year__in=self.request.GET.getlist('year')) | Q(genres__in=self.request.GET.getlist('genre')))
    #     return queryset

class AddStarRating(View):
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                event_id=int(request.POST.get('event')),
                defaults={'star_id': int(request.POST.get('star'))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class Search(ListView):
    def get_queryset(self):
        return Event.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = self.request.GET.get('q')
        return context




