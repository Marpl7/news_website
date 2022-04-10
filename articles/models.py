from django.db import models
from django.db import transaction


class Article(models.Model):

    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение',)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=256, verbose_name='Тэг')
    article = models.ManyToManyField(Article, related_name='tag', through='ArticleScope')

    def __str__(self):
        return self.name


class ArticleScope(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='scopes')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='scopes')
    is_main = models.BooleanField()

    # def save(self, *args, **kwargs):
    #     if self.is_main:
    #         try:
    #             temp = ArticleScope.objects.get(is_main=True)
    #             print(temp)
    #             if self != temp:
    #                 temp.is_main = False
    #                 temp.save()
    #         except ArticleScope.DoesNotExist:
    #             pass
    #     super(ArticleScope, self).save(*args, **kwargs)
    def save(self, *args, **kwargs):
        if not self.is_main:
            return super(ArticleScope, self).save(*args, **kwargs)
        with transaction.atomic():
            ArticleScope.objects.filter(is_main=True).update(is_main=False)
        return super(ArticleScope, self).save(*args, **kwargs)

