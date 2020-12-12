from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from apps.notification.utilities import create_notification

from .forms import ChirperProfileForm

def chirperprofile(request, username):
    user = get_object_or_404(User, username=username)
    chirps = user.chirps.all()

    for chirp in chirps:
        likes = chirp.likes.filter(created_by_id=request.user.id)

        if likes.count() > 0:
            chirp.liked = True
        else:
            chirp.liked = False

    context = {
        'user': user,
        'chirps': chirps
    }

    return render(request, 'chirperprofile/chirperprofile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ChirperProfileForm(request.POST, request.FILES, instance=request.user.chirperprofile)

        if form.is_valid():
            form.save()

            return redirect('chirperprofile', username=request.user.username)
    else:
        form = ChirperProfileForm(instance=request.user.chirperprofile)

    context = {
        'user': request.user,
        'form': form
    }

    return render(request, 'chirperprofile/edit_profile.html', context)


@login_required
def follow_chirper(request, username):
    user = get_object_or_404(User, username=username)

    request.user.chirperprofile.follows.add(user.chirperprofile)

    create_notification(request, user, 'follower')

    return redirect('chirperprofile', username=username)

@login_required
def unfollow_chirper(request, username):
    user = get_object_or_404(User, username=username)

    request.user.chirperprofile.follows.remove(user.chirperprofile)

    return redirect('chirperprofile', username=username)

def followers(request, username):
    user = get_object_or_404(User, username=username)

    return render(request, 'chirperprofile/followers.html', {'user': user})


def follows(request, username):
    user = get_object_or_404(User, username=username)

    return render(request, 'chirperprofile/follows.html', {'user': user})
