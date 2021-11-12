from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from .forms import ProfileForm
from .models import UserProfile, Follow
from post.models import Post

# Create your views here.

User = get_user_model()


@login_required(login_url='account:Login')
def UserProfileView(request, user):
    context = {}
    context['Followed'] = False

    user_profile = get_object_or_404(UserProfile, user=user)
    user_posts = Post.objects.filter(user=user)

    USER_PROFILE = UserProfile.objects.filter(followed_to__id=user)

    Follow_requests = Follow.objects.filter(to_user=request.user)
    context['Follow_requests'] = Follow_requests
    if USER_PROFILE.exists():
        context['Followed'] = True

    context['user_posts'] = user_posts
    context['user'] = user_profile
    return render(request, 'UserProfile.html', context)


def Complete_Profile(request):
    context = {}
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES or None)
        context['form'] = form

        if form.is_valid():
            name = form.cleaned_data['name']
            contact = form.cleaned_data['contact']
            organizer = form.cleaned_data['organizer']
            profile_image = form.cleaned_data['profile_image']

            user = UserProfile(
                user=request.user,
                profile_image=profile_image,
                name=name,
                contact=contact
            )
            user.save()

            user = UserProfile.objects.get(user=request.user)

            # If User applied for Organizer then intially user should be unverified but if User didn't applied for Organizer then user is a Verified user.
            if organizer == False:
                user.is_verified = True
                user.organizer = False

            elif organizer == True:
                user.organizer = True
                user.is_verified = False
                messages.info(
                    request, "Your request of becoming an Organizer is sent to Managing Team. You will be confirmed very soon. Thanks for applying")

            user.save()

            messages.success(request, "Profile Completed")
            return redirect('account:UserProfile', request.user.id)

    form = ProfileForm()
    context['form'] = form

    return render(request, 'Complete_Profile.html', context)


def Update_Profile(request, user):
    context = {}
    user = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST or None, instance=user)
        context['form'] = form
        username = request.POST.get('username')
        email = request.POST.get('email')

        if form.is_valid():
            form.save()

            request.user.username = username
            request.user.email = email

            request.user.save()

            messages.success(request, "Profile Updated")
            return redirect('account:UserProfile', request.user.id)

    form = ProfileForm(instance=user)
    context['form'] = form

    return render(request, 'UpdateProfile.html', context)


def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if username != '' and len(pass1) > 5:
            if pass1 == pass2:
                user = User.objects.create_user(
                    username=username, email=email, password=pass1)
                user.save()
                messages.success(request, "Account Created Successfully.")

                login_user = auth.authenticate(
                    username=username, password=pass1)
                if login_user is not None:
                    auth.login(request, login_user)
                    messages.success(request, "Logged in Successfully.")
                    return redirect('account:Complete_Profile')
                else:
                    messages.error(
                        request, "Something went Wrong. Please try to Login manually.")
                    return redirect('account:Login')
            else:
                messages.info(request, "Password didn't matched.")
                return redirect('account:Signup')
        else:
            messages.info(
                request, "Some Fields are empty. Please Fill out all the Fields.")
            return redirect('account:Signup')

    return render(request, 'signup.html')


def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username != '':
            login_user = auth.authenticate(
                username=username, password=password)
            if login_user is not None:
                auth.login(request, login_user)
                messages.success(request, "Logged in Successfully.")
                return redirect('core:Home')
            else:
                messages.error(
                    request, "Something went Wrong. Please try to Login again.")
                return redirect('account:Login')
        else:
            messages.info(
                request, "Some Fields are empty. Please Fill out all the Fields.")
            return redirect('account:Login')
    return render(request, 'login.html')


def Logout(request):
    auth.logout(request)

    messages.success(request, "Logged Out Successfully.")
    return redirect('core:Home')


@login_required(login_url='account:Login')
def FollowUser(request, to_user):
    follow_to_user = User.objects.get(id=to_user)

    follow_user = Follow(from_user=request.user,
                         to_user=follow_to_user, timestamp=timezone.now())

    # To Prevent Duplicate Request
    user_profile = UserProfile.objects.filter(
        user=request.user, followed_to__id=to_user)
    if user_profile.exists() == False:

        # It checks If the User already followed Another User. So It will only add user to their Particular List
        if UserProfile.objects.filter(user=to_user, followed_to=request.user).exists():
            # It adds request.user to User Follower List
            follow_to_user.userprofile.followers.add(request.user)
            follow_to_user.userprofile.save()

            # It adds User to request.user Followng List
            request.user.userprofile.followed_to.add(follow_to_user)
            request.user.userprofile.save()
            messages.info(request, f"You followed back {follow_to_user}")

        else:
            # It adds User to request.user Followng List
            request.user.userprofile.followed_to.add(follow_to_user)
            request.user.userprofile.save()

            # It adds request.user to User Follower List
            follow_to_user.userprofile.followers.add(request.user)
            follow_to_user.userprofile.save()

            follow_user.save()

            messages.info(request, f"You followed {follow_to_user}")
    else:
        # It removes User from request.user's Following List
        request.user.userprofile.followed_to.remove(follow_to_user)
        request.user.userprofile.save()

        # It removes request.user from User Follower List
        follow_to_user.userprofile.followers.remove(request.user)
        follow_to_user.userprofile.save()

    return redirect('account:UserProfile', to_user)


def Follow_back_user(request, requestID):
    try:
        Follow_request = Follow.objects.get(id=requestID)
        if Follow_request.to_user == request.user:
            request.user.userprofile.followed_to.add(Follow_request.from_user)
            request.user.userprofile.save()

            Follow_request.from_user.userprofile.followers.add(request.user)
            Follow_request.from_user.userprofile.save()

            Follow_request.delete()

            messages.success(
                request, f"You Followed back {Follow_request.from_user}. You are Friends Now.")
        else:
            messages.error(
                request, "You do not have the Permisions to do that.")
    except ObjectDoesNotExist:
        messages.error(request, f"Follow Request does not exists.")

    return redirect('account:UserProfile', request.user.id)


def delete_request(request, requestID):
    follow_request = get_object_or_404(Follow, id=requestID)
    if follow_request.to_user == request.user:
        follow_request.delete()

    return redirect('account:UserProfile', request.user.id)
