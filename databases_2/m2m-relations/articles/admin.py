from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scope, Tag


class RelationshipInlineFormset(BaseInlineFormSet):

    def to_python(self, value):
        if not value:
            return []
        return value.split(',')

    def validate(self, value):
        if self.forms is None:
            return
        count = 0
        for form in self.forms:
            if form.cleaned_data is None:
                return
            if form.cleaned_data.get('is_main'):
                count += 1
        if count != 1:
            raise ValidationError('Основны может быть только одно значение')
        super().validate()  # вызываем базовый код переопределяемого метода

    def clean(self):
        if self.forms is None:
            return
        count = 0
        array_count = []
        for form in self.forms:
            tag = form.cleaned_data.get('tag')
            if tag is None:
                continue
            array_count.append(tag.topic)
            if form.cleaned_data is None:
                return
            if form.cleaned_data.get('is_main'):
                count += 1
        if len(array_count) != len(set(array_count)):
            raise ValidationError('У вас дублируются теги')
        if count != 1:
            raise ValidationError('Основным может быть только одно значение')

        return super().clean()


class ScopeInLine(admin.TabularInline):
    model = Scope
    extra = 3
    formset = RelationshipInlineFormset
    can_delete = False
    min_num = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInLine, ]


@admin.register(Tag)
class Tag(admin.ModelAdmin):
    inlines = [ScopeInLine, ]
