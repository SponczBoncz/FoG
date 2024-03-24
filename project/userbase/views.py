import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, RedirectView, View
from django.urls import reverse_lazy
from django.contrib.auth import login, logout

from django.shortcuts import render, get_object_or_404, redirect

from .forms import LoginForm, UserCreationForm, AddInvitationForm, EditInvitationForm, LuckyShotForm
from .models import User, Game, GameInvitation

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def my_view(request):
    '''
    Description:
        This is a view function that renders the 'my_template.html' template for an authenticated user.

    Decorator:
        @login_required
    '''

    return render(request, 'userbase/my_template.html')

class LoginView(FormView):
    '''
    Description:
        This is a class-based view for handling user login. It renders the 'login.html' template and logs the user in upon successful form submission.

    Variables:
        template_name, form_class, success_url

    Methods:
        form_valid: Logs in the user upon successful form submission.
    '''

    template_name = 'userbase/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('all-games')

    def form_valid(self, form):
        user = form.user
        login(self.request, user)
        return super().form_valid(form)

class LogoutView(RedirectView):
    '''
    Description:
        This class-based view handles user logout functionality and redirects to the 'all-games' page.
    Variables:
        url
    '''

    url = reverse_lazy('all-games')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)

class UserCreationView(FormView):
    '''
    Description:
        Class-based view for user registration. It renders the 'user_creation.html' template and creates a new user upon form submission.

    Variables:
        template_name, form_class, success_url

    Methods:
        form_valid: Saves the new user upon successful form submission.
    '''

    template_name = 'userbase/user_creation.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        return redirect(self.success_url)

class UserCollectionView(LoginRequiredMixin, View):
    '''
    Description:
        This view displays the collection of games belonging to the logged-in user.

    Variables:
        template_name, login_url

    Methods:
        get: Retrieves the collection of games for the logged-in user.
    '''

    template_name = 'userbase/user_collection.html'
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        user_games = self.request.user.games.all()
        return render(request, self.template_name, {'user_games': user_games})

class AddGameToCollectionView(LoginRequiredMixin, View):
    '''
    Description:
        View for adding a game to the user's collection.

    Variables:
        template_name, login_url

    Methods:
        post: Adds the selected game to the user's collection.
    '''

    template_name = 'user-collection'
    login_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        game_pk = self.kwargs['game_pk']
        game = get_object_or_404(Game, pk=game_pk)
        request.user.games.add(game)
        return redirect(self.template_name)

class DeleteGameFromCollectionView(LoginRequiredMixin, View):
    '''
    Description:
        View for deleting a game from the user's collection.

    Variables:
        template_name, login_url

    Methods:
        post: Deletes the selected game from the user's collection.
    '''

    template_name = 'user-collection'
    login_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        game_pk = self.kwargs['game_pk']
        game = get_object_or_404(Game, pk=game_pk)
        request.user.games.remove(game)
        return redirect(self.template_name)

class UserInvitationsView(LoginRequiredMixin, View):
    '''
    Description:
        View for displaying user invitations, available places, and managing invitations.

    Variables:
        template_name, login_url

    Methods:
        get: Retrieves user invitations, available places, and invitations accepted by the user.
    '''

    template_name = 'userbase/user_invitations.html'
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        user_invitations = GameInvitation.objects.filter(user=self.request.user).order_by('game_time')
        # Calculate available places for each invitation in user_invitations
        for invitation in user_invitations:
            invitation.available_places = invitation.no_players - invitation.players.count()
        not_user_invitations = GameInvitation.objects.exclude(user=self.request.user)
        available_user_invitations = not_user_invitations.exclude(players=self.request.user).order_by('game_time')
        # Calculate available places for each invitation in available_user_invitations
        for invitation in available_user_invitations:
            invitation.available_places = invitation.no_players - invitation.players.count()
        invitations_accepted = not_user_invitations.filter(players=self.request.user).order_by('game_time')
        # Calculate available places for each invitation in invitations_accepted
        for invitation in invitations_accepted:
            invitation.available_places = invitation.no_players - invitation.players.count()
        return render(
            request,
            self.template_name,
            {
                'user_invitations': user_invitations,
                'available_user_invitations': available_user_invitations,
                'invitations_accepted': invitations_accepted
            }
        )

class AddInvitationView(LoginRequiredMixin, View):
    '''
    Description:
        View for adding a new game invitation.

    Variables:
        form_class, template_name, login_url

    Methods:
        get: Renders the form for adding a new game invitation.
        post: Processes the form submission for adding a new game invitation.
    '''

    form_class = AddInvitationForm
    template_name = 'userbase/add_invitation.html'
    login_url = reverse_lazy('login')


    def get(self, request, *args, **kwargs):
        # Pass the current user to the form
        form = self.form_class(user=request.user)
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Pass the current user to the form instead of request.POST
        form = self.form_class(user=request.user, data=request.POST)
        context = {"form": form}
        if form.is_valid():
            # Set the user field to the currently logged-in user before saving
            invitation = form.save(commit=False)
            invitation.user = request.user
            invitation = form.save()
            return redirect(
                'invitation-details',
                invitation_pk=invitation.pk,
            )
        else:
            return render(request, self.template_name, context)

class UserInvitationDetailsView(LoginRequiredMixin, View):
    '''
    Description:
        View for displaying details of a specific game invitation.

    Variables:
        template_name, login_url

    Methods:
        get: Retrieves and renders the details of a specific game invitation.
        post: Processes the form submission for joining or leaving a game invitation.
    '''

    template_name = 'userbase/invitation_details.html'
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        invitation_pk = self.kwargs['invitation_pk']
        invitation = get_object_or_404(GameInvitation, pk=invitation_pk)
        return render(request, self.template_name, {'invitation': invitation})

    def post(self, request, *args, **kwargs):
        invitation_pk = self.kwargs['invitation_pk']
        invitation = get_object_or_404(GameInvitation, pk=invitation_pk)

        if 'player_pk' in self.kwargs:
            player_pk = self.kwargs['player_pk']
            player = get_object_or_404(User, pk=player_pk)
            invitation.players.remove(player)
            text = f'Usunięto gracza {player.nick} z gry!'
        else:
            invitation.players.add(self.request.user)
            text = f'Dodano Cię do gry!'
        invitation.save()
        return render(
            request,
            'userbase/invitation_details.html',
            {'invitation': invitation, 'text': text})


class EditInvitationView(LoginRequiredMixin, View):
    '''
    Description:
        View for editing a game invitation.

    Variables:
        form_class, template_name, login_url

    Methods:
        get: Renders the form for editing a game invitation.
        post: Processes the form submission for editing a game invitation.
    '''

    form_class = EditInvitationForm
    template_name = 'userbase/edit_invitation.html'
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        # Get the invitation object
        invitation_pk = kwargs['invitation_pk']
        invitation = get_object_or_404(GameInvitation, pk=invitation_pk)

        # Pass the instance to the form
        form = self.form_class(user=request.user, instance=invitation)

        context = {
            "form": form,
            "invitation": invitation
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Get the invitation object
        invitation_pk = kwargs['invitation_pk']
        invitation = get_object_or_404(GameInvitation, pk=invitation_pk)

        # Pass the instance and data to the form
        form = self.form_class(user=request.user, data=request.POST, instance=invitation)
        context = {"form": form}

        if form.is_valid():
            # Set the user field to the currently logged-in user before saving
            invitation = form.save(commit=False)
            invitation.user = request.user
            invitation.save()
            return redirect('invitation-details', invitation_pk=invitation.pk)
        else:
            return render(request, self.template_name, context)

class DeleteInvitationView(View):
    '''
    Description:
        View for deleting a game invitation.

    Variables:
        template_name, login_url

    Methods:
        get: Renders the confirmation page for deleting a game invitation.
        post: Deletes the selected game invitation.
    '''

    template_name = 'userbase/delete_invitation.html'
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        invitation_pk = self.kwargs['invitation_pk']
        invitation = get_object_or_404(GameInvitation, pk=invitation_pk)
        return render(request, self.template_name, {'invitation': invitation})

    def post(self, request, *args, **kwargs):
        invitation_pk = kwargs['invitation_pk']
        invitation = get_object_or_404(GameInvitation, id=invitation_pk)
        invitation.delete()
        return redirect('user-invitations')

class LuckyShotView(LoginRequiredMixin, View):
    '''
    Description:
    View for a lucky shot game where the user can find a random game based on the number of players.

    Variables:
    form_class, template_name, login_url

    Methods:
        get: Renders the form for selecting the number of players.
        post: Processes the form submission to find a random game.
    '''

    form_class = LuckyShotForm
    template_name = 'userbase/lucky_shot.html'
    login_url = reverse_lazy('login')


    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            no_players = form.cleaned_data['no_players']
            games = request.user.games.filter(min_players__lte=no_players, max_players__gte=no_players)
            random_game = random.choice(games) if games else None
            context = {"form": form, "random_game": random_game}
            return render(request, self.template_name, context)
        else:
            context = {"form": form}
            return render(request, self.template_name, context)