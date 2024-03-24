from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import UserManager
from gamelist.models import Game


class User(AbstractBaseUser, PermissionsMixin):
    '''
    Attributes:
        email: EmailField - Stores the email address of the user. It is unique.
        is_superuser: BooleanField - Indicates if the user is a superuser. Default value is False.
        nick: CharField - Stores the nickname of the user, with a maximum length of 64 characters. It is unique.
        password: CharField - Stores the password of the user.
        admin: BooleanField - Indicates if the user is an admin. Default value is False.
        games: ManyToManyField - Relates the user to multiple Game objects. Can be blank.
        date_joined: DateTimeField - Stores the date and time when the user joined. Default value is the current time.

    Properties:
        USERNAME_FIELD = "email" - Specifies the field used as the unique identifier for the user (email).
        REQUIRED_FIELDS = [] - Indicates the required fields for creating a user instance.

    Methods:
        str(self) - Returns a string representation of the user object, using the email address as the output.

    Additional Information:
        Inherits from AbstractBaseUser and PermissionsMixin classes.
        Uses UserManager for managing user objects.
    '''

    email = models.EmailField(_("email address"), unique=True)
    is_superuser = models.BooleanField(default=False)
    nick = models.CharField(max_length=64, unique=True)
    password = models.CharField()
    admin = models.BooleanField(default=False)
    games = models.ManyToManyField(Game, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class GameInvitation(models.Model):
    '''
    Attributes:
        user: ForeignKey to User - Stores the user who owns the invitation. On deletion, cascades to related objects.
        game: ForeignKey to Game - Stores the game associated with the invitation. On deletion, cascades to related objects.
        no_players: IntegerField - Stores the number of players for the game invitation. Default value is 1.
        game_time: DateTimeField - Stores the date and time of the game. Default value is the current time.
        game_place: CharField - Stores the place/location of the game with a maximum length of 64 characters.
        players: ManyToManyField to User - Relates multiple users as invited players for the game. Can be blank.
        extra_text: CharField - Stores additional text related to the invitation with a maximum length of 510 characters. Can be blank.

    Methods:
        str(self) - Returns a string representation of the game invitation object, using the associated game as the output.
    '''

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invitation_owner")
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    no_players = models.IntegerField(default=1)
    game_time = models.DateTimeField(default=timezone.now)
    game_place = models.CharField(max_length=64)
    players = models.ManyToManyField(User, blank=True, related_name="invited_players")
    extra_text = models.CharField(max_length=510, blank=True)

    def __str__(self):
        return self.game