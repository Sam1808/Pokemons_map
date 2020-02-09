from django.db import models

# your models here

class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='pokemon', blank=True)

    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField()
    level = models.IntegerField(default = 0)
    health = models.IntegerField(default = 0)
    strength = models.IntegerField(default = 0)
    defence = models.IntegerField(default = 0)
    stamina = models.IntegerField(default = 0)