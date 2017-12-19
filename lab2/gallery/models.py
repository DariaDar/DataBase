from django.db import models

"""
class Visiting(models.Model):
    date = models.DateTimeField()
    painting = models.ForeignKey("Painting")
    visitor = models.ForeignKey("Visitor")


class Visitor(models.Model):
    name = models.CharField(max_length=35)
    email = models.EmailField()


class Exhibition(models.Model):
    country = models.CharField()
    city = models.CharField()


class Painting(models.Model):
    artist = models.ForeignKey("Artist")
    exhibition = models.ForeignKey("Exhibition")
    name = models.CharField(max_length=50)
    creation_date = models.DateField()
    style = models.CharField(max_length=50)
    techique = models.CharField(max_length=50)


class Artist(models.Model):
    name = models.CharField(max_length=50)
    birthdate = models.DateField()
    birthplace = models.CharField(max_length=50)
    biography = models.TextField()"""

