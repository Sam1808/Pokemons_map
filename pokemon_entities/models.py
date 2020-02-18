from django.db import models

class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    image = models.ImageField(verbose_name='Картинка')
    title_en = models.CharField(max_length=200, blank=True, verbose_name='Название (анг.)')
    title_jp = models.CharField(max_length=200, blank=True, verbose_name='Название (яп.)')
    description = models.TextField(blank=True, verbose_name='Описание')
    previous_evolution = models.ForeignKey('self',
                                           null=True,
                                           blank=True,
                                           on_delete=models.SET_NULL,
                                           related_name='next_evolution',
                                           verbose_name='Эволюция')



    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Покемон')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(verbose_name='Время появления')
    disappeared_at = models.DateTimeField(verbose_name='Время исчезновения')
    level = models.IntegerField(blank = True, null=True, verbose_name='Уровень')
    health = models.IntegerField(blank = True, null=True, verbose_name='Здоровье')
    strength = models.IntegerField(blank = True, null=True, verbose_name='Сила')
    defence = models.IntegerField(blank = True, null=True, verbose_name='Защита')
    stamina = models.IntegerField(blank = True, null=True, verbose_name='Выносливость')