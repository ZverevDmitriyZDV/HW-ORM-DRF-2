from django.db import models


class TopicTag(models.Model):
    topic = models.CharField(max_length=256, verbose_name='Наименование Тэга')

    class Meta:
        verbose_name = 'Наименование Тэга'
        verbose_name_plural = 'Наименование Тэга'

    def __str__(self):
        return self.topic


class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение', )
    scopes = models.ManyToManyField(TopicTag, through='Scope')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ('-published_at',)

    def __str__(self):
        return self.title


class Scope(models.Model):
    tag = models.ForeignKey(TopicTag, null=True, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, null=True, on_delete=models.CASCADE)
    is_main = models.BooleanField(verbose_name='Основной', default=False)

    class Meta:
        verbose_name = 'Соотношение Тэга к Статье'
        verbose_name_plural = 'Соотношение Тэга к Статье'
        ordering = ('-is_main',)

