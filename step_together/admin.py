from django import forms
from django.contrib import admin
from django.utils.html import format_html, format_html_join
from .models import AgreementCondition, ProviderAgrees, Agreement, TextQuestion


@admin.register(ProviderAgrees)
class ProviderAgreesAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ('provider_name', 'provider_organization', 'agreement_date')


class AgreementConditionInline(admin.TabularInline):  # type: ignore[type-arg]
    model = AgreementCondition
    extra = 1

class TextQuestionInline(admin.TabularInline):  # type: ignore[type-arg]
    model = TextQuestion
    extra = 1

# admin panel for managing agreements (and their versions), questions, etc.
@admin.register(Agreement)
class AgreementAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ('agreement_version_date', 'current',)
    inlines = [AgreementConditionInline, TextQuestionInline]

