from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Politician,
    Party,
    Office,
    Government,
    GovernmentOfficial,
    GovernmentParty,
    PoliticsParty,
)


@admin.register(Politician)
class PoliticianAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'title', 'age', 'photo_preview')
    search_fields = ('name', 'surname')

    def photo_preview(self, obj):
        if obj.photo_file:
            return format_html('<img src="{}" style="height:40px;"/>', obj.photo_file.url)
        return "-"
    photo_preview.short_description = 'Photo'


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'leader', 'founding', 'photo_preview')
    search_fields = ('name', 'leader')

    def photo_preview(self, obj):
        if obj.photo_file:
            return format_html('<img src="{}" style="height:40px;"/>', obj.photo_file.url)
        return "-"
    photo_preview.short_description = 'Photo'


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Government)
class GovernmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'in_function', 'prime_minister')
    search_fields = ('prime_minister',)


@admin.register(GovernmentOfficial)
class GovernmentOfficialAdmin(admin.ModelAdmin):
    list_display = ('id', 'government', 'politician', 'office', 'role', 'start_of_term', 'end_of_term')
    list_filter = ('role', 'start_of_term')


@admin.register(GovernmentParty)
class GovernmentPartyAdmin(admin.ModelAdmin):
    list_display = ('id', 'party', 'government')


@admin.register(PoliticsParty)
class PoliticsPartyAdmin(admin.ModelAdmin):
    list_display = ('id', 'politician', 'party', 'start_of_membership', 'end_of_membership')
