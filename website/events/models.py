from datetime import date

from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField('Категорія', max_length=255)
    description = models.TextField('Опис')
    url = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'


class Avtor(models.Model):
    name = models.CharField('Ім\'я', max_length=255)
    age = models.PositiveSmallIntegerField('Вік', default=0)
    description = models.TextField('Опис')
    image = models.ImageField('Фото', upload_to='avtors/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автори'
        verbose_name_plural = 'автори'

    def get_absolute_url(self):
        return reverse('avtor_detail', kwargs={'slug': self.name})


class SubCategory(models.Model):
    name = models.CharField('Ім\'я', max_length=255)
    description = models.TextField('Опис')
    url = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Підкатегорія'
        verbose_name_plural = 'Підкатегорії'


class Event(models.Model):
    title = models.CharField('Назва', max_length=255)
    tagline = models.CharField('Гасло', max_length=100, default='')
    description = models.TextField('Опис')
    poster = models.ImageField('Постер', upload_to='events/')
    year = models.PositiveSmallIntegerField('Рік виходу', default=2023)
    country = models.CharField('Країна', max_length=255)
    directors = models.ManyToManyField(Avtor, verbose_name='Автор', related_name='film_director')
    avtors = models.ManyToManyField(Avtor, verbose_name='Співавтор', related_name='film_avtor')
    genres = models.ManyToManyField(SubCategory, verbose_name='Підкатегорія')
    world_premiere = models.DateField('Дата виходу', default=date.today)
    budget = models.PositiveIntegerField('Ціль', default=0, help_text='in $')
    fees_in_USA = models.PositiveIntegerField('Збори в США', default=0, help_text='in $')
    fees_in_world = models.PositiveIntegerField('Збори в світі', default=0, help_text='in $')
    category = models.ForeignKey(Category, verbose_name='Категорія', on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=255, unique=True)
    draft = models.BooleanField('Чорновик', default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'slug': self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)


    class Meta:
        verbose_name = 'Івент'
        verbose_name_plural = 'Івенти'


class EventShots(models.Model):
    title = models.CharField('Заголовок', max_length=255)
    description = models.TextField('Опис')
    image = models.ImageField('Зображення', upload_to='event_shots/')
    event = models.ForeignKey(Event, verbose_name='Івент', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'


class RatingStar(models.Model):
    value = models.SmallIntegerField('Значення', default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = 'Зірка рейтингу'
        verbose_name_plural = 'Зірки рейтингу'
        ordering = ['-value']


class Rating(models.Model):
    ip = models.CharField('ІР адреса', max_length=255)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='зірка')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='івент')

    def __str__(self):
        return f"{self.star} - {self.event}"

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField('Ім\'я', max_length=255)
    text = models.TextField('Коментар', max_length=5000)
    parent = models.ForeignKey('self', verbose_name='Батько', on_delete=models.SET_NULL, blank=True, null=True)
    event = models.ForeignKey(Event, verbose_name='івент', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.event}"

    class Meta:
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'
