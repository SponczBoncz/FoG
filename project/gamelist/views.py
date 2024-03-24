import requests
from bs4 import BeautifulSoup
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from gamelist.models import (
    Game,
    Category,
    GameMechanic,
    RequestedMechanic,
    RequestedCategory,
    STATUS_CHOICES,
)
from django.forms import formset_factory, modelformset_factory
from gamelist.forms import (
    AddGameForm,
    EditGameForm,
    AddMechanicForm,
    AddCategoryForm,
    AskForCategoryForm,
    AskForMechanicForm,
    EditCategoryForm,
    EditMechanicForm,
    SearchGameForm,
    AddNewMechanicForm,
    AddNewCategoryForm,
)


class BaseGameListView(View):
    '''
    Description:
        This view renders a list of all games.

    Variables:
        template_name: Template used for rendering the view.
        games: Queryset of all games ordered by title.

    Methods:
        get: Renders a list of all games. Retrieves all games from the database and orders them by title.
            Renders the template specified by template_name with the games queryset.
    '''
    template_name = 'gamelist/all_games_list.html'

    def get(self, request, *args, **kwargs):
        games = Game.objects.order_by('title')
        return render(request, self.template_name, {'games': games})


class GameDetailView(View):
    '''
    Description:
        This view displays details of a specific game, including an image fetched from the game's BoardGameGeek link.

    Variables:
        game: The game object fetched from the database.
        game_image_url: The URL of the game image fetched from BoardGameGeek.

    Methods:
        get: Displays details of a specific game, including an image fetched from the game's BoardGameGeek link.
            Retrieves the game object based on the provided game_pk.
            Fetches the HTML content of the game's BoardGameGeek link and extracts the image URL using BeautifulSoup.
            Renders the game_details.html template with the game object.
    '''

    def get(self, request, *args, **kwargs):
        game_pk = self.kwargs['game_pk']
        game = get_object_or_404(Game, pk=game_pk)
        # Fetch the HTML content of the bgg_link page
        response = requests.get(game.bgg_link)
        if response.status_code == 200:
            html_content = response.text

            # Use BeautifulSoup to parse HTML and find the image URL
            soup = BeautifulSoup(html_content, 'html.parser')
            meta_tag = soup.find('meta', property='og:image')
            if meta_tag:
                game_image_url = meta_tag.get('content')
                game.image_url = game_image_url  # Store the image URL in the model
        return render(request, 'gamelist/game_details.html', {'game': game})

class AddGameView(View):
    '''
    Description:
    This view allows users to add a new game.

    Variables:
        form_class: Form used for adding a game.
        template_name: Template used for rendering the view.
        form: Form instance for adding a game.

    Methods:
        get: Renders the form for adding a new game.
            Instantiates the AddGameForm and passes it to the template specified by template_name.
            post: Handles the submission of the form for adding a new game.
            Validates the form data, saves the game if the form is valid, and redirects to the game details page.
            If the form is invalid, renders the template with the form containing validation errors.
    '''

    form_class = AddGameForm
    template_name = "gamelist/add_game.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {"form": form}
        if form.is_valid():
            game = form.save()
            return redirect(
                'game-details',
                game_pk=game.pk,
            )
        else:
            return render(request, self.template_name, context)


class GameMechanicView(View):
    '''
    Description:
    This view displays details of a specific game mechanic.

    Variables:
        mechanic: The game mechanic object fetched from the database.

    Methods:
        get: Displays details of a specific game mechanic.
            Retrieves the game mechanic object based on the provided mechanic_pk.
            Renders the mechanic_details.html template with the game mechanic object.
    '''

    def get(self, request, *args, **kwargs):
        mechanic_pk = self.kwargs['mechanic_pk']
        mechanic = get_object_or_404(GameMechanic, pk=mechanic_pk)
        return render(request, 'gamelist/mechanic_details.html', {'mechanic': mechanic})

class CategoryView(View):
    '''
    Description:
        This view displays details of a specific category.

    Variables:
        category: The category object fetched from the database.

    Methods:
        get: Displays details of a specific category.
            Retrieves the category object based on the provided category_pk.
            Renders the category_details.html template with the category object.
    '''

    def get(self, request, *args, **kwargs):
        category_pk = self.kwargs['category_pk']
        category = get_object_or_404(Category, pk=category_pk)
        return render(request, 'gamelist/category_details.html', {'category': category})

class MechanicListView(View):
    '''
    Description:
        This view renders a list of all game mechanics.

    Variables:
        mechanics: Queryset of all game mechanics ordered by name.

    Methods:
        get: Renders a list of all game mechanics.
            Retrieves all game mechanics from the database and orders them by name.
            Renders the mechanics_list.html template with the mechanics queryset.
    '''

    def get(self, request, *args, **kwargs):
        mechanics = GameMechanic.objects.order_by('name')
        return render(request, 'gamelist/mechanics_list.html', {'mechanics': mechanics})

class CategoryListView(View):
    '''
    Description:
        This view renders a list of all categories.

    Variables:
        categories: Queryset of all categories ordered by name.

    Methods:
        get: Renders a list of all categories.
            Retrieves all categories from the database and orders them by name.
            Renders the categories_list.html template with the categories queryset.
    '''

    def get(self, request, *args, **kwargs):
        categories = Category.objects.order_by('name')
        return render(request, 'gamelist/categories_list.html', {'categories': categories})

class EditGameView(View):
    '''
    Description:
        This view allows users to edit details of a specific game.

    Variables:
        form_class: Form used for editing a game.
        template_name: Template used for rendering the view.
        game: The game object fetched from the database.
        form: Form instance for editing the game.

    Methods:
        get: Allows users to edit details of a specific game.
            Retrieves the game object based on the provided game_pk and renders the form for editing the game details.
        post: Handles the submission of the form for editing a game.
            Validates the form data, saves the changes if the form is valid, and redirects to the game details page.
            If the form is invalid, renders the template with the form containing validation errors.
    '''

    form_class = EditGameForm
    template_name = 'gamelist/edit_game.html'

    def get(self, request, *args, **kwargs):
        game_pk = kwargs['game_pk']
        game = get_object_or_404(Game, id=game_pk)
        form = self.form_class(instance=game)
        context = {
            "form":form,
            "game":game
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        game_pk = kwargs['game_pk']
        game = get_object_or_404(Game, id=game_pk)
        form = self.form_class(request.POST, instance=game)
        if form.is_valid():
            form.save()(
                'game-details',
                game_pk=game.pk,
            )
        else:
            context = {
                "form": form,
                "game": game
            }
            return render(request, self.template_name, context)


class AddMechanicView(View):
    '''
    Description:
        This view allows users to add a new game mechanic.

    Variables:
        form_class: Form used for adding a game mechanic.
        template_name: Template used for rendering the view.
        pending_mechanics: Queryset of pending game mechanics ordered by name.
        formset: Formset for adding pending game mechanics.

    Methods:
        get: Allows users to add a new game mechanic.
            Retrieves pending game mechanics from the database, creates a formset for adding pending mechanics,
            and renders the formset in the add_mechanic.html template.
        post: Handles the submission of the form for adding a new game mechanic.
            Validates the formset data, creates new game mechanics if the formset is valid,
            and redirects to the mechanic list page.
            If the formset is invalid, renders the template with the formset containing validation errors.
    '''

    form_class = AddMechanicForm
    template_name = "gamelist/add_mechanic.html"

    def get(self, request, *args, **kwargs):
        pending_mechanics = RequestedMechanic.objects.filter(status=0).order_by('name')
        formset = modelformset_factory(RequestedMechanic, form=AddMechanicForm, extra=0)
        mechanic_forms = formset(queryset=pending_mechanics)
        context = {
            "mechanic_forms": mechanic_forms
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        formset = modelformset_factory(RequestedMechanic, form=AddMechanicForm, extra=0)
        mechanic_forms = formset(request.POST)

        if mechanic_forms.is_valid():
            for form in mechanic_forms:
                if form.cleaned_data['status'] == 1:
                    mechanic = form.save(commit=False)
                    GameMechanic.objects.create(
                        name=mechanic.name,
                        description=mechanic.description,
                    )
                    RequestedMechanic.objects.filter(pk=mechanic.pk).delete()
                elif form.cleaned_data['status'] == 2:
                    mechanic = form.save(commit=False)
                    RequestedMechanic.objects.filter(pk=mechanic.pk).status = 2
                    mechanic.save()
            return redirect('mechanic-list')
        else:
            context = {
                "mechanic_forms": mechanic_forms
            }
            return render(request, self.template_name, context)


class AddCategoryView(View):
    '''
    Description:
        This view allows users to add a new category.

    Variables:
        form_class: Form used for adding a category.
        template_name: Template used for rendering the view.
        pending_categories: Queryset of pending categories ordered by name.
        formset: Formset for adding pending categories.

    Methods:
        get: Allows users to add a new category.
            Retrieves pending categories from the database, creates a formset for adding pending categories,
            and renders the formset in the add_category.html template.
        post: Handles the submission of the form for adding a new category.
            Validates the formset data, creates new categories if the formset is valid,
            and redirects to the category list page.
            If the formset is invalid, renders the template with the formset containing validation errors.
    '''

    form_class = AddCategoryForm
    template_name = "gamelist/add_category.html"

    def get(self, request, *args, **kwargs):
        pending_categories = RequestedCategory.objects.filter(status=0).order_by('name')
        formset = modelformset_factory(RequestedCategory, form=AddCategoryForm, extra=0)
        category_forms = formset(queryset=pending_categories)
        context = {
            "category_forms": category_forms
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        formset = modelformset_factory(RequestedCategory, form=AddCategoryForm, extra=0)
        category_forms = formset(request.POST)

        if category_forms.is_valid():
            for form in category_forms:
                if form.cleaned_data['status'] == 1:
                    category = form.save(commit=False)
                    Category.objects.create(
                        name=category.name,
                        description=category.description,
                    )
                    RequestedCategory.objects.filter(pk=category.pk).delete()
                elif form.cleaned_data['status'] == 2:
                    category = form.save(commit=False)
                    RequestedCategory.objects.filter(pk=category.pk).status = 2
                    category.save()
            return redirect('category-list')
        else:
            context = {
                "category_forms": category_forms
            }
            return render(request, self.template_name, context)


class AddNewCategoryView(LoginRequiredMixin, View):
    '''
    Description:
        This view allows users to add a new category.

    Variables:
        form_class: Form used for adding a new category.
        template_name: Template used for rendering the view.
        form: Form instance for adding a new category.

    Methods:
        get: Renders the form for adding a new category.
            Instantiates the AddNewCategoryForm and passes it to the template.
        post: Handles the submission of the form for adding a new category.
            Validates the form data, saves the category if the form is valid, and redirects to the category details page.
            If the form is invalid, renders the template with the form containing validation errors.
    '''

    form_class = AddNewCategoryForm
    template_name = "gamelist/add_new_category.html"
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {"form": form}
        if form.is_valid():
            category = form.save()
            return redirect(
                'category-details',
                category_pk=category.pk,
            )
        else:
            return render(request, self.template_name, context)

class AddNewMechanicView(LoginRequiredMixin, View):
    '''
    Description:
        This view allows users to add a new game mechanic.

    Variables:
        form_class: Form used for adding a new game mechanic.
        template_name: Template used for rendering the view.
        form: Form instance for adding a new game mechanic.

    Methods:
        get: Renders the form for adding a new game mechanic.
            Instantiates the AddNewMechanicForm and passes it to the template.
        post: Handles the submission of the form for adding a new game mechanic.
            Validates the form data, saves the mechanic if the form is valid, and redirects to the mechanic details page.
            If the form is invalid, renders the template with the form containing validation errors.
    '''

    form_class = AddNewMechanicForm
    template_name = "gamelist/add_new_mechanic.html"
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {"form": form}
        if form.is_valid():
            mechanic = form.save()
            return redirect(
                'mechanic-details',
                mechanic_pk=mechanic.pk,
            )
        else:
            return render(request, self.template_name, context)


class AskForCategoryView(View):
    '''
    Description:
        This view allows users to request a new category.

    Variables:
        form_class: Form used for requesting a new category.
        template_name: Template used for rendering the view.
        form: Form instance for requesting a new category.

    Methods:
        get: Renders the form for requesting a new category.
            Instantiates the AskForCategoryForm and passes it to the template.
        post: Handles the submission of the form for requesting a new category.
            Validates the form data, saves the requested category if the form is valid,
            and redirects to the category list page.
            If the form is invalid, renders the template.
    '''

    form_class = AskForCategoryForm
    template_name = "gamelist/ask_for_category.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            requested_category = form.save()
            return redirect(
                'category-list',
            )
        else:
            return render(request, self.template_name)

class AskForMechanicView(View):
    '''
    Description:
        This view allows users to request a new game mechanic.

    Variables:
        form_class: Form used for requesting a new game mechanic.
        template_name: Template used for rendering the view.
        form: Form instance for requesting a new game mechanic.

    Methods:
        get: Renders the form for requesting a new game mechanic.
            Instantiates the AskForMechanicForm and passes it to the template.
        post: Handles the submission of the form for requesting a new game mechanic.
            Validates the form data, saves the requested mechanic if the form is valid,
            and redirects to the mechanic list page.
            If the form is invalid, renders the template.
    '''
    form_class = AskForMechanicForm
    template_name = "gamelist/ask_for_mechanic.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            requested_mechanic = form.save()
            return redirect(
                'mechanic-list',
            )
        else:
            return render(request, self.template_name)

class EditCategoryView(View):
    '''
    Description:
        This view allows users to edit details of a specific category.

    Variables:
        form_class: Form used for editing a category.
        template_name: Template used for rendering the view.
        category: The category object fetched from the database.
        form: Form instance for editing the category.

    Methods:

        get: Retrieves the category object to be edited and renders the form for editing the category details.
        post: Handles the submission of the form for editing a category.
            Validates the form data, saves the changes if the form is valid,
            and redirects to the category details page.
            If the form is invalid, renders the template with the form containing validation errors.
    '''

    form_class = EditCategoryForm
    template_name = 'gamelist/edit_category.html'

    def get(self, request, *args, **kwargs):
        category_pk = kwargs['category_pk']
        category = get_object_or_404(Category, id=category_pk)
        form = self.form_class(instance=category)
        context = {
            "form":form,
            "category":category
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        category_pk = kwargs['category_pk']
        category = get_object_or_404(Category, id=category_pk)
        form = self.form_class(request.POST, instance=category)
        if form.is_valid():
            form.save()(
                'category-details',
                category_pk=category.pk,
            )
        else:
            context = {
                "form": form,
                "category": category
            }
            return render(request, self.template_name, context)

class EditMechanicView(View):
    '''
    Description:
        This view allows users to edit details of a specific game mechanic.

    Variables:
        form_class: Form used for editing a game mechanic.
        template_name: Template used for rendering the view.
        mechanic: The game mechanic object fetched from the database.
        form: Form instance for editing the game mechanic.

    Methods:
        get: Retrieves the game mechanic object to be edited and renders the form for editing the mechanic details.
        post: Handles the submission of the form for editing a game mechanic.
            Validates the form data, saves the changes if the form is valid,
            and redirects to the mechanic details page.
            If the form is invalid, renders the template with the form containing validation errors.
    '''

    form_class = EditMechanicForm
    template_name = 'gamelist/edit_mechanic.html'

    def get(self, request, *args, **kwargs):
        mechanic_pk = kwargs['mechanic_pk']
        mechanic = get_object_or_404(Category, id=mechanic_pk)
        form = self.form_class(instance=mechanic)
        context = {
            "form":form,
            "mechanic":mechanic
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        mechanic_pk = kwargs['mechanic_pk']
        mechanic = get_object_or_404(GameMechanic, id=mechanic_pk)
        form = self.form_class(request.POST, instance=mechanic)
        if form.is_valid():
            form.save()(
                'mechanic-details',
                mechanic_pk=mechanic.pk,
            )
        else:
            context = {
                "form": form,
                "mechanic": mechanic
            }
            return render(request, self.template_name, context)


class SearchGameView(ListView):
    '''
    Description:
        This view allows users to search for games based on title.

    Variables:
        template_name: Template used for rendering the view.
        games: Queryset of games filtered based on search query.
        search_query: Search query entered by the user.

    Methods:
        get_queryset: Retrieves the queryset of games based on the search query entered by the user.
        get_context_data: Adds the search query entered by the user to the context data.
    '''

    template_name = "gamelist/search.html"
    context_object_name = "games"
    paginate_by = 10

    def get_queryset(self):
        title = self.request.GET.get("title", "")
        return Game.objects.filter(title__icontains=title)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get("title", "")
        return context

class DeleteGameView(View):
    '''
    Description:
        This view handles the deletion of a game.

    Variables:
        template_name: Template used for rendering the delete game confirmation page.

    Methods:
        get: Retrieves the game object to be deleted and fetches its image URL from an external source.
            Renders the delete game confirmation page with the game object.
        post: Handles the deletion of the game object upon receiving a POST request.
    '''

    template_name = 'gamelist/delete_game.html'

    def get(self, request, *args, **kwargs):
        game_pk = self.kwargs['game_pk']
        game = get_object_or_404(Game, pk=game_pk)
        # Fetch the HTML content of the bgg_link page
        response = requests.get(game.bgg_link)
        if response.status_code == 200:
            html_content = response.text

            # Use BeautifulSoup to parse HTML and find the image URL
            soup = BeautifulSoup(html_content, 'html.parser')
            meta_tag = soup.find('meta', property='og:image')
            if meta_tag:
                game_image_url = meta_tag.get('content')
                game.image_url = game_image_url  # Store the image URL in the model
        return render(request, self.template_name, {'game': game})

    def post(self, request, *args, **kwargs):
        game_pk = kwargs['game_pk']
        game = get_object_or_404(Game, id=game_pk)
        game.delete()
        return redirect('all-games')


class DeleteGameMechanicView(View):
    '''
    Description:
        This view handles the deletion of a game mechanic.

    Variables:
        template_name: Template used for rendering the delete game mechanic confirmation page.

    Methods:
        get: Retrieves the game mechanic object to be deleted and renders the delete game mechanic confirmation page.
        post: Handles the deletion of the game mechanic object upon receiving a POST request.
    '''

    template_name = 'gamelist/delete_mechanic.html'

    def get(self, request, *args, **kwargs):
        mechanic_pk = self.kwargs['mechanic_pk']
        mechanic = get_object_or_404(GameMechanic, pk=mechanic_pk)
        return render(request, self.template_name, {'mechanic': mechanic})

    def post(self, request, *args, **kwargs):
        mechanic_pk = kwargs['mechanic_pk']
        mechanic = get_object_or_404(GameMechanic, id=mechanic_pk)
        mechanic.delete()
        return redirect('mechanic-list')

class DeleteCategoryView(View):
    '''
    Description:
        This view handles the deletion of a game category.

    Variables:
        template_name: Template used for rendering the delete game category confirmation page.

    Methods:
        get: Retrieves the game category object to be deleted and renders the delete game category confirmation page.
        post: Handles the deletion of the game category object upon receiving a POST request.
    '''

    template_name = 'gamelist/delete_category.html'

    def get(self, request, *args, **kwargs):
        category_pk = self.kwargs['category_pk']
        category = get_object_or_404(Category, pk=category_pk)
        return render(request, self.template_name, {'category': category})

    def post(self, request, *args, **kwargs):
        category_pk = kwargs['category_pk']
        category = get_object_or_404(Category, id=category_pk)
        category.delete()
        return redirect('category-list')