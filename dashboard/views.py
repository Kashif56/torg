from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from account.models import UserProfile

from core.models import Tournament, RegisteredTeams, Results
from core.forms import TournamentForm
# Create your views here.


@login_required(login_url='account:Login')
def dashboard_home(request):
    context = {}
    if request.user.userprofile.organizer and request.user.userprofile.is_verified:
        tournaments = Tournament.objects.filter(user=request.user)
        context['objects'] = tournaments
        return render(request, 'DashBoard/dashboard.html', context)
    else:
        messages.error(request, "Only Organizers can access Dashboard.")
        return redirect('core:Home')


def dashboard_tournament_detail(request, id):
    context = {}
    context['id'] = id
    if request.user.is_authenticated:
        if request.user.userprofile.organizer and request.user.userprofile.is_verified:
            try:
                tournament = Tournament.objects.get(user=request.user, id=id)
                tournaments = Tournament.objects.filter(user=request.user)
                context['objects'] = tournaments
                context['obj'] = tournament
            except ObjectDoesNotExist:
                messages.error(request, "Tourament does not exists.")
                return redirect('dashboard:dashboard_home')

            return render(request, 'DashBoard/dashboard_tournament_detail.html', context)
        else:
            messages.error(request, "Only Organizers can access Dashboard.")
            return redirect('core:Home')
    else:
        messages.error(request, "Please Login to access Dashboard.")
        return redirect('core:Home')


@login_required(login_url='account:Login')
def Create_Tournament(request):
    form = TournamentForm()
    tournaments = Tournament.objects.filter(user=request.user)
    if request.user.userprofile.organizer and request.user.userprofile.is_verified:
        if Tournament.objects.filter(user=request.user, is_active=True).exists() is not True:
            if request.method == 'POST':
                form = TournamentForm(request.POST, request.FILES)
                user = UserProfile.objects.get(user=request.user)
                if form.is_valid():

                    title = form.cleaned_data['title']
                    image = form.cleaned_data['image']
                    description = form.cleaned_data['description']
                    prize_pool = form.cleaned_data['prize_pool']
                    fee = form.cleaned_data['fee']
                    slots = form.cleaned_data['slots']
                    last_date = form.cleaned_data['last_date']

                    tournament = Tournament(
                        user=request.user,
                        title=title,
                        image=image,
                        description=description,
                        prize_pool=prize_pool,
                        fee=fee,
                        slots=slots,
                        last_date=last_date,
                        date_created=timezone.now()
                    )
                    day_diff = last_date - timezone.now()

                    # Checks if there are atleast 3 days for Registeration
                    if day_diff.days < 3:
                        messages.error(
                            request, f"Please Check Last Date. It should be 3 Days differnce.")
                        return redirect('dashboard:db_create_tournament')

                    tournament.save()

                    user.tournaments.add(tournament)
                    messages.success(request, "Tournament has been created.")
                    return redirect('dashboard:dashboard_home')
        else:
            messages.error(
                request, f"Dear {request.user.username}! According to the Terms and Conditions You can only Organize one tournament at once. You already have an Tournament whose current status is active. Please deactivate the Tournament to create another one.")
            return redirect('dashboard:dashboard_home')

    else:
        messages.error(
            request, f"Dear {request.user}! You can only create a tournament when you are registered as Organizer but currently you're not. or You are not yet Verified")
        return redirect('dashboard:dashboard_home')

    context = {
        'form': form,
        'objects': tournaments,
    }
    return render(request, 'DashBoard/dashboard_create_tournament.html', context)


@login_required(login_url='account:Login')
def dashboard_tournament_update(request, id):
    context = {}
    context['id'] = id
    if request.user.userprofile.organizer and request.user.userprofile.is_verified:
        tournaments = Tournament.objects.filter(user=request.user)
        context['objects'] = tournaments
        try:
            tournament = Tournament.objects.get(id=id)
            context['obj'] = tournament
            if request.user == tournament.user:
                form = TournamentForm(instance=tournament)
                context['form'] = form

                if request.method == 'POST':
                    form = TournamentForm(
                        request.POST, request.FILES, instance=tournament)
                    context['form'] = form
                    if form.is_valid():

                        form.save()

                        # Updating the Last time when user update its Tournament
                        tournament.last_updated = timezone.now()
                        tournament.save()

                        messages.success(
                            request, f"{tournament.title} was updated")
                        return redirect('dashboard:db_tournament_detail', id=tournament.id)
        except ObjectDoesNotExist:
            messages.error(
                request, f"Tournament with id {id} does not exixts.")
            return redirect('dashboard:db_tournament_detail', id=tournament.id)

    return render(request, 'DashBoard/dashboard_tournament_update.html', context)


@login_required(login_url='account:Login')
def dashboard_tournament_teams(request, t):
    context = {}
    context['title'] = t
    try:
        tournament = Tournament.objects.get(title=t)
        context['tournament'] = tournament
        tournaments = Tournament.objects.filter(user=request.user)
        context['objects'] = tournaments
    except ObjectDoesNotExist:
        messages.error(request, f"Tournament with id {id} does not exists.")
        return redirect('dashboard:db_tournament_detail', id=tournament.id)

    return render(request, 'DashBoard/dashboard_tournament_teams.html', context)


def dashboard_tournament_delete(request, id):
    try:
        obj = Tournament.objects.get(id=id)
        if request.user == obj.user:
            request.user.userprofile.tournaments.remove(obj)
            obj.delete()
            messages.success(request, "Tournament was deleted.")
            return redirect('dashboard:dashboard_home')
    except ObjectDoesNotExist:
        messages.error(request, "Tournament does not exists.")
        return redirect('dashboard:dashboard_home')


def dashboard_tournament_team_detail(request, tt, team_name):
    context = {}
    try:
        context['team_name'] = team_name
        tournament = Tournament.objects.get(title=tt)
        context['teams'] = tournament
        team = RegisteredTeams.objects.get(
            team_name=team_name, current_tournament=tournament)
        context['team'] = team
    except ObjectDoesNotExist:
        messages.error(request, f"Team does not exists")
        return redirect('dashboard:dashboard_home')
    return render(request, "DashBoard/dashboard_tournament_team_detail.html", context)


@login_required(login_url='account:Login')
def remove_team(request, tournament, team_name):
    context = {}
    context['tournament'] = tournament
    context['team_name'] = team_name
    objects = Tournament.objects.filter(user=request.user)
    context['objects'] = objects
    if request.method == 'POST':
        try:
            tournament = Tournament.objects.get(title=tournament)
            context['tournament'] = tournament
            if request.user == tournament.user:

                # Getting the requested team to delete
                team = RegisteredTeams.objects.get(
                    current_tournament=tournament, team_name=team_name)
                context['team'] = team

                team.delete()
                messages.success(
                    request, f"{team_name} successfully removed from {tournament}")
                return redirect('dashboard:db_tournament_teams', tournament.title)
            else:
                messages.error(
                    request, "You do not have the permissions to remove team.")
                return redirect('dashboard:db_tournament_teams', tournament.title)
        except ObjectDoesNotExist:
            messages.error(request, "Something Went Wrong")
            return redirect('dashboard:db_tournament_teams', tournament.title)

    return render(request, 'DashBoard/team_delete_confirm.html', context)


def AcceptRegisteration(request, user_id, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    if tournament.user == request.user:
        try:
            team = RegisteredTeams.objects.get(
                user=user_id, current_tournament=tournament)
            team.is_registered = True
            team.save()
            messages.success(request, f"{team.team_name} is now Registered.")
            return redirect('dashboard:db_tournament_teams', tournament.title)

        except ObjectDoesNotExist:
            messages.success(request, f"Something Went Wrong!")
            return redirect('dashboard:db_tournament_team_detail', tt=tournament.title, team_name=team.team_name)

    else:
        messages.success(
            request, f"You don't have the permissions to do that.")
        return redirect('dashboard:db_tournament_team_detail', tt=tournament.title, team_name=team.team_name)


# Add Results
def add_results(request, tournamentID):
    context = {}

    tournament = get_object_or_404(Tournament, id=tournamentID)
    context['tournament'] = tournament
    tournaments = Tournament.objects.filter(user=request.user)
    context['objects'] = tournaments

    if request.method == 'POST':
        rank = request.POST.get('rank')
        team = request.POST.get('team')
        team = RegisteredTeams.objects.get(
            current_tournament=tournament, id=team)
        tournament = get_object_or_404(Tournament, id=tournamentID)
        date = timezone.now()

        if request.user == tournament.user:
            if Results.objects.filter(tournament=tournament, team=team).exists():
                messages.info(
                    request, f"{team} has already a standing assigned to it.")
                return redirect('dashboard:db_add_results', tournament.id)
            elif Results.objects.filter(tournament=tournament, rank=rank):
                messages.info(
                    request, f"Rank {rank} has already assigned to another Team.")
                return redirect('dashboard:db_add_results', tournament.id)

            result = Results(tournament=tournament,
                             team=team, rank=rank, date=date)

            result.save()
            tournament.results.add(result)
            tournament.save()

        else:
            messages.error(request, "You do not have the permissions.")
            return redirect('dashboard:db_add_results', tournament.id)

    return render(request, 'dashboard/dashboard_add_results.html', context)


def final_standings(request, tournamentID):
    context = {}
    tournament = get_object_or_404(Tournament, id=tournamentID)
    context['tournament'] = tournament
    return render(request, 'dashboard/dashboard_standings.html', context)
