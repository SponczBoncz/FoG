from django.db import models


STATUS_CHOICES = [
    (0, 'pending'),
    (1, 'accepted'),
    (2, 'not accepted'),
]

class Category(models.Model):
    '''
    Attributes:
        name: CharField with max length of 64 characters. Should be unique.
        description: TextField to provide additional information about the category.

    Methods:
        str: Returns the name of the category.
    '''

    name = models.CharField(max_length=64, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class GameMechanic(models.Model):
    '''
    Attributes:
        name: CharField with max length of 64 characters. Should be unique.
        description: TextField to provide additional information about the game mechanic.

    Methods:
        str: Returns the name of the game mechanic.
    '''

    name = models.CharField(max_length=64, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class Game(models.Model):
    '''
    Attributes:
        title: CharField with max length of 255 characters. Should be unique.
        author: CharField with max length of 255 characters.
        description: TextField to provide a detailed description of the game.
        min_players: IntegerField to specify the minimum number of players for the game.
        max_players: IntegerField to specify the maximum number of players for the game.
        game_time: CharField with max length of 64 characters to specify the estimated game time.
        category: Many-to-Many relationship with Category model.
        game_mechanics: Many-to-Many relationship with GameMechanic model.
        bgg_link: URLField to store the BoardGameGeek link for the game.

    Methods:
        str: Returns the title of the game.
    '''

    title = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255)
    description = models.TextField()
    min_players = models.IntegerField()
    max_players = models.IntegerField()
    game_time = models.CharField(max_length=64)
    category = models.ManyToManyField(Category)
    game_mechanics = models.ManyToManyField(GameMechanic)
    bgg_link = models.URLField()

    def __str__(self):
        return self.title

class RequestedMechanic(models.Model):
    '''
    Attributes:
        name: CharField with max length of 64 characters. Should be unique.
        description: TextField to provide additional information about the requested game mechanic.
        status: IntegerField with choices defined in STATUS_CHOICES (pending, accepted, not accepted). Default value is 0 (pending).

    Methods:
        str: Returns the name of the requested game mechanic.
    '''

    name = models.CharField(max_length=64, unique=True)
    description = models.TextField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

    def __str__(self):
        return self.name

class RequestedCategory(models.Model):
    '''
    Attributes:
        name: CharField with max length of 64 characters. Should be unique.
        description: TextField to provide additional information about the requested category.
        status: IntegerField with choices defined in STATUS_CHOICES (pending, accepted, not accepted). Default value is 0 (pending).

    Methods:
        str: Returns the name of the requested category.
    '''

    name = models.CharField(max_length=64, unique=True)
    description = models.TextField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

    def __str__(self):
        return self.name