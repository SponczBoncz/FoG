"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from gamelist import views as gamelist_view
from userbase import views as userbase_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('all_games/', gamelist_view.BaseGameListView.as_view(), name='all-games'),
    path('all_games/<int:game_pk>/', gamelist_view.GameDetailView.as_view(), name="game-details"),
    path('add_game/', gamelist_view.AddGameView.as_view(), name='add-game'),
    path('add_mechanic/', gamelist_view.AddMechanicView.as_view(), name='add-mechanic'),
    path('add_category/', gamelist_view.AddCategoryView.as_view(), name='add-category'),
    path('add_new_mechanic/', gamelist_view.AddNewMechanicView.as_view(), name='add-new-mechanic'),
    path('add_new_category/', gamelist_view.AddNewCategoryView.as_view(), name='add-new-category'),
    path('requested_category/', gamelist_view.AskForCategoryView.as_view(), name='requested-category'),
    path('requested_mechanic/', gamelist_view.AskForMechanicView.as_view(), name='requested-mechanic'),
    path('mechanic/<int:mechanic_pk>/', gamelist_view.GameMechanicView.as_view(), name='mechanic-details'),
    path('category/<int:category_pk>/', gamelist_view.CategoryView.as_view(), name='category-details'),
    path('mechanic/', gamelist_view.MechanicListView.as_view(), name='mechanic-list'),
    path('category/', gamelist_view.CategoryListView.as_view(), name='category-list'),
    path('edit_game/<int:game_pk>/', gamelist_view.EditGameView.as_view(), name='edit-game'),
    path('edit_category/<int:category_pk>/', gamelist_view.EditCategoryView.as_view(), name='edit-category'),
    path('edit_mechanic/<int:mechanic_pk>/', gamelist_view.EditMechanicView.as_view(), name='edit-mechanic'),
    path('login/', userbase_view.LoginView.as_view(), name='login'),
    path('logout/', userbase_view.LogoutView.as_view(), name='logout'),
    path('register/', userbase_view.UserCreationView.as_view(), name='register'),
    path('test/', userbase_view.my_view, name='test'),
    path('search/', gamelist_view.SearchGameView.as_view(), name='search'),
    path('delete_game/<int:game_pk>/', gamelist_view.DeleteGameView.as_view(), name='delete-game'),
    path('delete_mechanic/<int:mechanic_pk>/', gamelist_view.DeleteGameMechanicView.as_view(), name='delete-mechanic'),
    path('delete_category/<int:category_pk>/', gamelist_view.DeleteCategoryView.as_view(), name='delete-category'),
    path('delete_invitation/<int:invitation_pk>/', userbase_view.DeleteInvitationView.as_view(), name='delete-invitation'),
    path('user_collection/', userbase_view.UserCollectionView.as_view(), name='user-collection'),
    path('user_invitations/', userbase_view.UserInvitationsView.as_view(), name='user-invitations'),
    path('user_invitations/<int:invitation_pk>/', userbase_view.UserInvitationDetailsView.as_view(), name='invitation-details'),
    path('user_invitations/<int:invitation_pk>/', userbase_view.UserInvitationDetailsView.as_view(), name='accept-invitation'),
    path('user_invitations/<int:invitation_pk>/<int:player_pk>', userbase_view.UserInvitationDetailsView.as_view(), name='decline-player'),
    path('add_invitation/', userbase_view.AddInvitationView.as_view(), name='add-invitation'),
    path('edit_invitation/<int:invitation_pk>/', userbase_view.EditInvitationView.as_view(), name='edit-invitation'),
    path('user_collection/add/<int:game_pk>/', userbase_view.AddGameToCollectionView.as_view(), name='add-to-collection'),
    path('user_collection/delete/<int:game_pk>/', userbase_view.DeleteGameFromCollectionView.as_view(), name='delete-from-collection'),
    path('lucky_shot/', userbase_view.LuckyShotView.as_view(), name='lucky-shot'),
]
