from django.shortcuts import get_object_or_404, render, redirect

from .models import Bot, Game
from .forms import GameForm, BotForm


def index(request):
    return render(request, 'index.html')


def games_list(request):
    qs = Game.objects.all()
    return render(request, 'games_list.html', {'object_list': qs})


def bots_list(request):
    qs = Bots.objects.all()
    return render(request, 'bots_list.html', {'object_list': qs})


def bot_add(request):
    if request.method == 'POST':
        form = BotForm(request.POST, request.FILES)
        print form
        if form.is_valid():
            form.save()
            return redirect(bots_list)
    else:
        form = BotForm()
    return render(request, 'bot_add.html', {'form': form})


def game_add(request):
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(games_list)
    else:
        form = GameForm()
    return render(request, 'game_add.html', {'form': form})