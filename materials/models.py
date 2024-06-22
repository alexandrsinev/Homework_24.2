from django.db import models
NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    preview = models.ImageField(upload_to='preview/', verbose_name='Превью', **NULLABLE)
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title_lesson = models.CharField(max_length=200, verbose_name='Название урока')
    preview = models.ImageField(upload_to='preview/', verbose_name='Превью', **NULLABLE)
    description = models.TextField(verbose_name='Описание урока')
    url = models.URLField(max_length=300, verbose_name='ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Название курса')

    def __str__(self):
        return f'{self.title_lesson}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
