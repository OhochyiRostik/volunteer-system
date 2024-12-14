from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')
    list_display_links = ('name', )


class ReviewInLine(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ('name', 'email')


class EventShotsInline(admin.StackedInline):
    model = EventShots
    extra = 1
    readonly_fields = ('get_image', )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')

    get_image.short_description = 'Фото'


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'draft')
    list_display_links = ('title', )
    list_filter = ('category', 'year')
    search_fields = ('title', 'category__name')
    inlines = [EventShotsInline, ReviewInLine]
    save_on_top = True
    save_as = True
    list_editable = ('draft', )
    actions = ['publish', 'unpublish']
    readonly_fields = ('get_image', )
    # fields = (('avtors', 'genres', 'directors'), )
    fieldsets = (
        (None, {
            'fields': (('title', 'tagline'), )
        }),
        (None, {
            'fields': ('description', ('poster', 'get_image'))
        }),
        (None, {
            'fields': (('year', 'world_premiere', 'country'), )
        }),
        ('Avtors', {
            'fields': (('avtors', 'genres', 'directors', 'category'), )
        }),
        (None, {
            'fields': (('budget', 'fees_in_USA', 'fees_in_world'),)
        }),
        ('Option', {
            'fields': (('url', 'draft'),)
        }),
    )
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="50" height="60">')


    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запис оновлено"
        else:
            message_bit = f"{row_update} записи оновлено"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запис оновлено"
        else:
            message_bit = f"{row_update} записи оновлено"
        self.message_user(request, f"{message_bit}")

    publish.short_description = 'Опублікувати'
    publish.allowed_permission = ('change', )

    unpublish.short_description = 'Зняти з публікації'
    unpublish.allowed_permission = ('change', )

    get_image.short_description = 'Постер'

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'parent', 'event', 'id')
    readonly_fields = ('name', 'email')


@admin.register(SubCategory)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


@admin.register(Avtor)
class AvtorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'get_image')
    readonly_fields = ('get_image', )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')

    get_image.short_description = 'Фото'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('event', 'ip')


@admin.register(EventShots)
class EventShotsAdmin(admin.ModelAdmin):
    list_display = ('title', 'event', 'get_image')
    readonly_fields = ('get_image', )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')

    get_image.short_description = 'Фото'



@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    list_display = ('value', )
# admin.site.register(Category)
# admin.site.register(Genre)
# admin.site.register(Event)
# admin.site.register(EventShots)
# admin.site.register(Avtor)
# admin.site.register(Rating)
# admin.site.register(RatingStar)
# admin.site.register(Reviews)


admin.site.site_title = 'Сторінка адміністрування'
admin.site.site_header = 'Сторінка адміністрування'
