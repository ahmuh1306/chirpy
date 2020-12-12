from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Chirp

@login_required
def feed(request):
    userids = [request.user.id]

    for chirper in request.user.chirperprofile.follows.all():
        userids.append(chirper.user.id)

    chirps = Chirp.objects.filter(created_by_id__in=userids)

    for chirp in chirps:
        likes = chirp.likes.filter(created_by_id=request.user.id)

        if likes.count() > 0:
            chirp.liked = True
        else:
            chirp.liked = False

    return render(request, 'feed/feed.html', {'chirps': chirps})

@login_required
def search(request):
    query = request.GET.get('query', '')

    if len(query) > 0:
        chirpers = User.objects.filter(username__icontains=query)
        chirps = Chirp.objects.filter(body__icontains=query)
    else:
        chirpers = []
        chirps = []

    context = {
        'query': query,
        'chirpers': chirpers,
        'chirps': chirps
    }

    return render(request, 'feed/search.html', context)