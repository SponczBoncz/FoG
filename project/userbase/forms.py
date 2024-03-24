from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User, GameInvitation, Game

class LoginForm(forms.Form):
    """
    Description:
        Form for user login.

    Fields:
        email: CharField for user email.
        password: CharField for user password.

    Methods:
        clean: Custom validation method to authenticate the user.
    """

    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('email')
        password = cleaned_data.get('password')
        self.user = authenticate(username=username, password=password)
        if self.user is None:
            raise ValidationError("Nieprawidłowe hasło lub email")



class UserCreationForm(UserCreationForm):
    '''
    Description:
        Form for user registration.

    Fields:
        nick: CharField for user nickname.
        email: CharField for user email.
        password1: CharField for user password.
        password2: CharField for password confirmation.
    '''

    class Meta:
        model = User
        fields = ['nick', 'email', 'password1', 'password2']  # Include email, password1, and password2 fields
        # fields = ("email",)


class UserChangeForm(UserChangeForm):
    '''
    Description:
        Form for user profile editing.

    Fields:
        nick: CharField for user nickname.
        email: CharField for user email.
        password: CharField for user password.
    '''

    class Meta:
        model = User
        fields = ['nick', 'email', 'password']  # Include email, password1, and password2 fields




class AddInvitationForm(forms.ModelForm):
    '''
    Description:
        Form for adding a game invitation.

    Fields:
        game: Select field for selecting a game from the user's connected games.
        no_players: Integer field for specifying the number of players.
        game_time: CharField for specifying the game time.
        game_place: CharField for specifying the game place.
        extra_text: CharField for additional text.

    Customization:
        Filters games based on the current user's connected games.
        Sets widget attributes for input validation.
    '''

    class Meta:
        model = GameInvitation
        fields = [
            'game',
            'no_players',
            'game_time',
            'game_place',
            'extra_text'
        ]


    def __init__(self, user, *args, **kwargs):
        super(AddInvitationForm, self).__init__(*args, **kwargs)


        # Set the widget for the 'game' field to CheckboxSelectMultiple
        self.fields['game'].widget = forms.Select()
        # Filter games based on the current user's connected games
        self.fields['game'].queryset = user.games.all()
        self.fields['no_players'].widget.attrs['min'] = 1
        self.fields['game_time'].widget.attrs['maxlength'] = 255
        self.fields['game_place'].widget.attrs['maxlength'] = 255
        self.fields['extra_text'].widget.attrs['maxlength'] = 510


class EditInvitationForm(forms.ModelForm):
    '''
    Description:
        Form for editing a game invitation.

    Fields:
        game: Select field for selecting a game from the user's connected games.
        no_players: Integer field for specifying the number of players.
        game_time: CharField for specifying the game time.
        game_place: CharField for specifying the game place.
        extra_text: CharField for additional text.

    Customization:
        Filters games based on the current user's connected games.
        Sets widget attributes for input validation.
    '''

    class Meta:
        model = GameInvitation
        fields = [
            'game',
            'no_players',
            'game_time',
            'game_place',
            'extra_text'
        ]

    def __init__(self, user, *args, **kwargs):
        super(EditInvitationForm, self).__init__(*args, **kwargs)

        # Set the widget for the 'game' field to Select
        self.fields['game'].widget = forms.Select()

        # Filter games based on the current user's connected games
        self.fields['game'].queryset = user.games.all()

        self.fields['no_players'].widget.attrs['min'] = 1
        self.fields['game_time'].widget.attrs['maxlength'] = 255
        self.fields['game_place'].widget.attrs['maxlength'] = 255
        self.fields['extra_text'].widget.attrs['maxlength'] = 510


class LuckyShotForm(forms.ModelForm):
    '''
    Description:
        Form for selecting the number of players for a lucky shot game.

    Fields:
        no_players: Integer field for specifying the number of players.

    Customization:
        Sets a custom validation rule for the number of players.

    '''

    # Custom field for number of players
    no_players = forms.IntegerField(min_value=1)

    class Meta:
        model = Game
        fields = []




