from django import forms

from django.core.validators import URLValidator

from .models import Game, Category, GameMechanic, RequestedCategory, RequestedMechanic, STATUS_CHOICES


class AddGameForm(forms.ModelForm):
    '''
    Description:
        Form for adding a new game to the system.

    Fields:
        title: CharField for the game title.
        author: CharField for the game author.
        description: TextField for the game description.
        min_players: IntegerField for the minimum number of players.
        max_players: IntegerField for the maximum number of players.
        game_time: CharField for specifying the game time.
        category: CheckboxSelectMultiple for selecting game categories.
        game_mechanics: CheckboxSelectMultiple for selecting game mechanics.
        bgg_link: URLInput for specifying a BoardGameGeek link.

    Customization:
        Sets widget attributes for input validation.
    '''

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
        self.fields['category'].queryset = Category.objects.order_by('name')
        self.fields['game_mechanics'].widget = forms.CheckboxSelectMultiple()
        self.fields['game_mechanics'].queryset = GameMechanic.objects.order_by('name')
        self.fields['bgg_link'].widget = forms.URLInput()

class EditGameForm(forms.ModelForm):
    '''
    Description:
        Form for editing an existing game.

    Fields:
        Same as AddGameForm.

    Customization:
        Sets initial values for fields based on the current values in the model instance.
    '''

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
        self.fields['category'].queryset = Category.objects.order_by('name')
        self.fields['game_mechanics'].widget = forms.CheckboxSelectMultiple()
        self.fields['game_mechanics'].queryset = GameMechanic.objects.order_by('name')
        self.fields['bgg_link'].widget = forms.URLInput()

class AddMechanicForm(forms.ModelForm):
    '''
    Description:
        Form for adding a new game mechanic.

    Fields:
        name: CharField for the mechanic name.
        description: TextField for the mechanic description.
        status: ChoiceField for selecting the status of the mechanic.

    Customization:
        Sets widget attributes for input validation.
    '''

    class Meta:
        model = RequestedMechanic
        fields = [
            'name',
            'description',
            'status'
        ]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')  # Get the instance from kwargs
        super(AddMechanicForm, self).__init__(*args, **kwargs)

        if instance:
            # Set the initial value for each field based on the current value in the model instance
            for field_name in self.fields:
                self.fields[field_name].widget.attrs['value'] = getattr(instance, field_name)

        self.fields['name'].widget.attrs['maxlength'] = 255
        self.fields['description'].widget = forms.Textarea()
        status = forms.ChoiceField(choices=STATUS_CHOICES)


class AddCategoryForm(forms.ModelForm):
    '''
    Description:
        Form for adding a new game category.

    Fields:
        Same as AddMechanicForm.

    Customization:
        Same as AddMechanicForm.
    '''

    class Meta:
        model = RequestedCategory
        fields = [
            'name',
            'description',
            'status'
        ]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')  # Get the instance from kwargs
        super(AddCategoryForm, self).__init__(*args, **kwargs)

        if instance:
            # Set the initial value for each field based on the current value in the model instance
            for field_name in self.fields:
                self.fields[field_name].widget.attrs['value'] = getattr(instance, field_name)

        self.fields['name'].widget.attrs['maxlength'] = 255
        self.fields['description'].widget = forms.Textarea()
        status = forms.ChoiceField(choices=STATUS_CHOICES)


class AddNewCategoryForm(forms.ModelForm):
    '''
    Description:
        Form for adding a new category.

    Fields:
        Same as AddMechanicForm.

    Customization:
        Same as AddMechanicForm.
    '''

    class Meta:
        model = Category
        fields = [
            'name',
            'description'
        ]

    def __init__(self, *args, **kwargs):
        super(AddNewCategoryForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['maxlength'] = 255
        self.fields['description'].widget = forms.Textarea()


class AddNewMechanicForm(forms.ModelForm):
    '''
    Description:
        Form for adding a new game mechanic.

    Fields:
        Same as AddMechanicForm.

    Customization:
        Same as AddMechanicForm.
    '''

    class Meta:
        model = GameMechanic
        fields = [
            'name',
            'description'
        ]

    def __init__(self, *args, **kwargs):
        super(AddNewMechanicForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['maxlength'] = 255
        self.fields['description'].widget = forms.Textarea()


class AskForCategoryForm(forms.ModelForm):
    '''
    Description:
        Form for requesting a new game category.

    Fields:
        Same as AddMechanicForm.

    Customization:
        Same as AddMechanicForm.
    '''

    class Meta:
        model = RequestedCategory
        fields = [
            'name',
            'description'
        ]

    def __init__(self, *args, **kwargs):
        super(AskForCategoryForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['maxlength'] = 255
        self.fields['description'].widget = forms.Textarea()

class AskForMechanicForm(forms.ModelForm):
    '''
    Description:
        Form for requesting a new game mechanic.

    Fields:
        Same as AddMechanicForm.

    Customization:
        Same as AddMechanicForm.
    '''

    class Meta:
        model = RequestedMechanic
        fields = [
            'name',
            'description'
        ]

    def __init__(self, *args, **kwargs):
        super(AskForMechanicForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['maxlength'] = 255
        self.fields['description'].widget = forms.Textarea()


class EditCategoryForm(forms.ModelForm):
    '''
    Description:
        Form for editing an existing game category.

    Fields:
        Same as AddMechanicForm.

    Customization:
        Same as AddMechanicForm.
    '''

    class Meta:
        model = Category
        fields = ['name',
                  'description',
                  ]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')  # Get the instance from kwargs
        super(EditCategoryForm, self).__init__(*args, **kwargs)

        # Set the initial value for each field based on the current value in the model instance
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['value'] = getattr(instance, field_name)

        self.fields['name'].widget.attrs['maxlength'] = 255
        self.fields['description'].widget = forms.Textarea()


class EditMechanicForm(forms.ModelForm):
    '''
    Description:
        Form for editing an existing game mechanic.

    Fields:
        Same as AddMechanicForm.

    Customization:
        Same as AddMechanicForm.
    '''

    class Meta:
        model = GameMechanic
        fields = ['name',
                  'description',
                  ]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')  # Get the instance from kwargs
        super(EditMechanicForm, self).__init__(*args, **kwargs)

        # Set the initial value for each field based on the current value in the model instance
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['value'] = getattr(instance, field_name)

        self.fields['name'].widget.attrs['maxlength'] = 255
        self.fields['description'].widget = forms.Textarea()


class SearchGameForm(forms.Form):
    '''
    Description:
        Form for searching games based on title.

    Fields:
        title: CharField for entering the game title.
    '''

    title = forms.CharField(max_length=255)