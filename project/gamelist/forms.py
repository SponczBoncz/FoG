from django import forms

from django.core.validators import URLValidator

from .models import Game, Category, GameMechanic


class AddGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = [
            'title',
            'author',
            'description',
            'min_players',
            'max_players',
            'game_time',
            'category',
            'game_mechanics',
            'bgg_link'
        ]

    def __init__(self, *args, **kwargs):
        super(AddGameForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['maxlength'] = 255
        self.fields['author'].widget.attrs['maxlength'] = 255
        self.fields['description'].widget = forms.Textarea()
        self.fields['min_players'].widget.attrs['min'] = 1
        self.fields['max_players'].widget.attrs['min'] = 1
        self.fields['game_time'].widget.attrs['maxlength'] = 64
        self.fields['category'].widget = forms.CheckboxSelectMultiple()
        self.fields['category'].queryset = Category.objects.all()
        self.fields['game_mechanics'].widget = forms.CheckboxSelectMultiple()
        self.fields['game_mechanics'].queryset = GameMechanic.objects.all()
        self.fields['bgg_link'].widget = forms.URLInput()

class EditGameForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = ['title',
                  'author',
                  'description',
                  'min_players',
                  'max_players',
                  'game_time',
                  'category',
                  'game_mechanics',
                  'bgg_link'
                  ]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')  # Get the instance from kwargs
        super(EditGameForm, self).__init__(*args, **kwargs)

        # Set the initial value for each field based on the current value in the model instance
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['value'] = getattr(instance, field_name)

        self.fields['title'].widget.attrs['maxlength'] = 255
        self.fields['author'].widget.attrs['maxlength'] = 255
        self.fields['description'].widget = forms.Textarea()
        self.fields['min_players'].widget.attrs['min'] = 1
        self.fields['max_players'].widget.attrs['min'] = 1
        self.fields['game_time'].widget.attrs['maxlength'] = 64
        self.fields['category'].widget = forms.CheckboxSelectMultiple()
        self.fields['category'].queryset = Category.objects.all()
        self.fields['game_mechanics'].widget = forms.CheckboxSelectMultiple()
        self.fields['game_mechanics'].queryset = GameMechanic.objects.all()
        self.fields['bgg_link'].widget = forms.URLInput()
