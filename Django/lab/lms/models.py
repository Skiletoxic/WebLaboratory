from distutils.command import sdist
from django.db import models
from django.utils import timezone
from datetime import datetime

STATUS_CHOICE= (('Готов','Готово'),
                ('Не готов','Не готово'))
SEX = (('М','Мужской'),
       ('Ж','Женский'))
NORMA = (('Отрицательно','Отрицательно'),
         ('В норме','В норме'),
         ('Титр меньше 250','Титр меньше 250'),
         ('Титр меньше 150','Титр меньше 150'),
         ('0 - 10','0 - 10'),
         ('0 - 13.6','0 - 13.6'),
         ('0 - 1','0 - 1'),
         ('менее 50','менее 50'),
         ('0.2 - 0.6','0.2 - 0.6'),
          )
# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=1000)
class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)


class Structure(models.Model):
    name= models.CharField(max_length=255, null=True, blank=True, verbose_name='Подразделение')
    
    def __str__(self):
        return f'{self.name}.'

    class Meta:
        ordering = ['name']
        verbose_name = 'Подразделение'
        verbose_name_plural= 'Подразделения'


class Price(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    bio = models.CharField(max_length=255, null=True, blank=True, verbose_name='Анализ')
    day = models.CharField(max_length=255, null=True, blank=True, verbose_name='Срок готовности')
    norma = models.CharField(max_length=255, choices=NORMA, null=True, blank=True, verbose_name='Нормы')
    price = models.IntegerField(null=True, blank=True, verbose_name='Цена')

    def __str__(self):
        return f'{self.name}.'

    class Meta:
        ordering = ['name']
        verbose_name = 'Прайс'
        verbose_name_plural= 'Прайс'


class Journal(models.Model):
    number = models.IntegerField(null=True, blank=True, verbose_name='Номер заявки')
    client_name = models.CharField(max_length=255, verbose_name='Имя')
    client_surname = models.CharField(max_length=255, verbose_name='Фамилия')
    client_phone = models.IntegerField(null=True, blank=True, verbose_name='Телефон')
    birth = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    sex = models.CharField(max_length=10, choices=SEX, null=True, blank=True, verbose_name='Пол')
    analysis_name = models.ManyToManyField(Price, verbose_name='название анализа')
    analysis_cathegory = models.ManyToManyField(Structure, verbose_name='Подразделение')
    date_time = models.DateTimeField(default=timezone.now, null=True, blank=True, verbose_name='Дата создания')
    is_done = models.CharField(max_length=10, choices=STATUS_CHOICE, default='Не готов', verbose_name='Статус')
    description = models.TextField(null=True, blank=True, verbose_name='Результат анализов')
    norma = models.CharField(max_length=255, choices=NORMA, null=True, blank=True, verbose_name='Нормы')

    def __str__(self):
        return f'Номер заявки: {self.number}, Клиент: {self.client_name} {self.client_surname}'
 
    class Meta:
        verbose_name = 'Журнал заявок'
        verbose_name_plural= 'Журнал заявок'    