from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.mail import send_mail
from torg.settings import EMAIL_HOST_USER

import datetime

from post.models import Post

from .forms import TournamentForm, TeamsRegisterationForm
from .models import Tournament, RegisteredTeams, Comment
from account.models import UserProfile
# Create your views here.

current_date = timezone.now()

one_week_ago = datetime.datetime.today() - datetime.timedelta(days=7)


def Home(request):
    if request.user.is_authenticated:
        if request.user.userprofile.organizer == True and request.user.userprofile.is_verified == True:
            return redirect('dashboard:dashboard_home')
        else:
            return redirect('core:Tournaments')

    return render(request, 'index.html')


def Tournaments(request):
    context = {}
    tournaments = Tournament.objects.filter(
        is_active=True, last_date__gt=current_date).order_by('-is_featured')
    context['tournaments'] = tournaments

    # FILTERS on GET request
    upload_date = request.GET.get('upload_date')
    game_mode = request.GET.get('game_mode')
    context['game_mode'] = game_mode
    context['upload_date'] = upload_date
    print(one_week_ago)
    query_result = []
    if upload_date == 'this_week' and game_mode == '':
        query_result = Tournament.objects.filter(
            Q(is_active=True) &
            Q(date_created__gte=one_week_ago)
        )
    elif upload_date == 'this_month' and game_mode == '':
        query_result = Tournament.objects.filter(
            Q(is_active=True) &
            Q(date_created__month=current_date.month)
        )
    elif upload_date == 'this_year' and game_mode == '':
        query_result = Tournament.objects.filter(
            Q(is_active=True) &
            Q(date_created__year=current_date.year)
        )
    elif upload_date == 'this_week' and game_mode != '':
        query_result = Tournament.objects.filter(
            Q(is_active=True) &
            Q(game_mode=game_mode) &
            Q(date_created__gte=one_week_ago)
        )
    elif upload_date == 'this_month' and game_mode != '':
        query_result = Tournament.objects.filter(
            Q(is_active=True) &
            Q(game_mode=game_mode) &
            Q(date_created__month=current_date.month)
        )
    elif upload_date == 'this_year' and game_mode != '':
        query_result = Tournament.objects.filter(
            Q(is_active=True) &
            Q(date_created__year=current_date.year) &
            Q(game_mode=game_mode)

        )

    else:
        query_result = Tournament.objects.filter(
            is_active=True, game_mode=game_mode
        )
    context['query_result'] = query_result
    print(query_result)
    return render(request, 'tournament.html', context)


def Tournament_Detail(request, id):
    context = {}
    context['registered'] = False
    context['pending_registeration'] = False
    context['liked'] = False
    try:
        tournament = Tournament.objects.get(id=id)
        context['tournament'] = tournament

        if request.user.is_authenticated:
            # If user had liked the Tournament already
            liked_tournament = tournament.likes.filter(id=request.user.id)
            if liked_tournament.exists():
                context['liked'] = True

            pending_registeration = RegisteredTeams.objects.filter(
                user=request.user,
                current_tournament=tournament,
                is_registered=False).exists()

            registered = RegisteredTeams.objects.filter(
                user=request.user,
                current_tournament=tournament,
                is_registered=True).exists()

            # If registeration is in Pending
            if pending_registeration == True:
                context['pending_registeration'] = True

            # If team registeration is accepted by Organizer
            elif registered == True:
                context['registered'] = True

    except ObjectDoesNotExist:
        messages.error(request, f"Tournament with id {id} does not exists")
        return redirect('core:Tournaments')

    return render(request, 'tournament-detail.html', context)


@login_required(login_url='account:Login')
def RegisterTeam(request, id):
    context = {}
    try:
        tournament = Tournament.objects.get(id=id)

        user = UserProfile.objects.get(user=request.user)
        context['tournament'] = tournament
        if tournament.last_date > current_date:
            if tournament.is_active == True:
                filter_duplicate = RegisteredTeams.objects.filter(
                    user=request.user,
                    current_tournament=tournament,
                    is_registered=True)

                pending_payment = RegisteredTeams.objects.filter(
                    user=request.user,
                    current_tournament=tournament,
                    is_registered=False)
                if filter_duplicate.exists() is not True:
                    if pending_payment.exists() is not True:
                        if request.method == 'POST':
                            form = TeamsRegisterationForm(request.POST or None)
                            context['form'] = form

                            if form.is_valid():
                                team_name = form.cleaned_data['team_name']
                                team_number = form.cleaned_data['team_number']

                                player1_ign = form.cleaned_data['player1_ign']

                                player2_ign = form.cleaned_data['player2_ign']

                                player3_ign = form.cleaned_data['player3_ign']

                                player4_ign = form.cleaned_data['player4_ign']

                                player5_ign = form.cleaned_data['player5_ign']

                                registered_team = RegisteredTeams(
                                    user=request.user,
                                    current_tournament=tournament,
                                    team_name=team_name,
                                    team_number=team_number,
                                    player1_ign=player1_ign,

                                    player2_ign=player2_ign,

                                    player3_ign=player3_ign,

                                    player4_ign=player4_ign,

                                    player5_ign=player5_ign,

                                    date_registered=current_date
                                )

                                if tournament.slots >= 1:
                                    if user.organizer != True:
                                        # Saving In Database
                                        registered_team.save()
                                        tournament.teams.add(
                                            registered_team)
                                        user.registered_in_tournaments.add(
                                            tournament)
                                        post = Post(
                                            user=request.user,
                                            title=f"I have registered in {tournament.title}.",
                                            image=tournament.image,
                                            timestamp=current_date
                                        )
                                        post.save()

                                        # Sending Email to Organizer
                                        subject = f"Regisetration to be Confirmed"
                                        message = f"{team_name} has registered for {tournament.title}. Please Head back to your Dashboard to Confirm their entry in the tournament."

                                        to_user = request.user.email

                                        send_mail(
                                            subject, message, EMAIL_HOST_USER, [to_user], fail_silently=False)

                                        print("Email Sent")

                                        messages.info(
                                            request, "Team registered Successfully. Please wait for confirmation from Tournament Organizer.")
                                        return redirect('core:Tournament_Detail', id=tournament.id)

                                    else:
                                        messages.info(
                                            request, f"Dear {request.user.username}! You cannot register in any tournament until you are registered as Organizer")

                                        return redirect('core:Tournament_Detail', id=tournament.id)

                                else:
                                    messages.info(
                                        request, f"Dear {request.user.username}! We are very sorry as slots were limited. So currently there is no slot available.")
                                    return redirect('core:Tournament_Detail', id=tournament.id)

                    else:
                        messages.error(
                            request, f"Dear {request.user.username}! You have registered your team in this Tournament but didn't confirmed by Organizer. Please wait until Tournament Organizer confirms your entry.")
                        return redirect('core:Home')
                else:
                    messages.error(
                        request, f"You have already registered a team in {tournament.title}")
                    return redirect('core:Home')

                form = TeamsRegisterationForm()
                context['form'] = form
            else:
                messages.info(
                    request, "This Tournament is currently not active")
                return redirect('core:Home')
        else:
            messages.error(request, "This Tournament is closed Now.")
            return redirect('core:Tournament_Detail', id=tournament.id)

        return render(request, 'register.html', context)

    except ObjectDoesNotExist:
        messages.error(request, "Tournament with this id doesn't exists.")
        return redirect('core:Home')


@login_required(login_url='account:Login')
def CancelRegisteration(request, id):
    try:
        tournament = Tournament.objects.get(id=id)
        user = UserProfile.objects.get(user=request.user)
        team_in_tournament = RegisteredTeams.objects.get(
            user=request.user, current_tournament=tournament)

        user.registered_in_tournaments.remove(tournament)
        team_in_tournament.delete()
        messages.success(request, "Your registeration has been cancelled.")
        return redirect('core:Home')

    except ObjectDoesNotExist:
        messages.error(request, "The Tournament with this id does not exixts.")
        return redirect('core:Home')


def about_us(request):
    return render(request, 'about.html')


def RegisteredTeamsView(request, tournament_id):
    context = {}
    try:
        tournament = Tournament.objects.get(id=tournament_id)
        context['tournament'] = tournament

        teams = tournament.teams.all()
        context['teams'] = teams
    except ObjectDoesNotExist:
        messages.error(request, "Tournament with this ID does not Exists.")
        return redirect('core:Tournament_Detail', id=tournament.id)

    return render(request, 'RegisteredTeams.html', context)


def TournamentQueryView(request, query):
    context = {}
    context['query'] = query
    if query == 'Free':
        tournaments = Tournament.objects.filter(
            is_active=True, last_date__gt=current_date, fee__lt=1).order_by('-is_featured')
        context['tournaments'] = tournaments
    elif query == 'Paid':
        tournaments = Tournament.objects.filter(
            is_active=True, last_date__gt=current_date, fee__gt=0).order_by('-is_featured')
        context['tournaments'] = tournaments

    return render(request, 'Tournament_Query.html', context)


@login_required(login_url='account:Login')
def LikeTournament(request, tournamentID):
    tournament = get_object_or_404(Tournament, id=tournamentID)

    if tournament.likes.filter(id=request.user.id):
        tournament.likes.remove(request.user)

    else:
        tournament.likes.add(request.user)
        messages.info(request, f"You Liked the {tournament.title}")

    return redirect('core:Tournament_Detail', tournamentID)


def AddComment(request, tournamentID):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        tournament = get_object_or_404(Tournament, id=tournamentID)
        user = request.user
        timestamp = timezone.now()

        new_comment = Comment(user=user, tournament=tournament,
                              comment=comment, timestamp=timestamp)

        new_comment.save()

        tournament.comments.add(new_comment)
        tournament.save()

        messages.success(request, "Comment Added")

    return redirect('core:Tournament_Detail', tournamentID)


def delete_comment(request, commentID, tournamentID):
    tournament = get_object_or_404(Tournament, id=tournamentID)
    comment = get_object_or_404(Comment, id=commentID)

    if comment.user == request.user:
        comment.delete()
    return redirect('core:Tournament_Detail', tournamentID)


def final_standings(request, tournamentID):
    context = {}
    tournament = get_object_or_404(Tournament, id=tournamentID)
    context['tournament'] = tournament
    context['standings'] = tournament.results.all()
    return render(request, 'FinalStandings.html', context)
