from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import Http404
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods

from coins.constants import CAPSULE_PRICE


@login_required
def coins(request: HttpRequest) -> HttpResponse:
    return render(request, template_name='coins/coins_page.html')


@login_required
def collect_capsule(request: HttpRequest) -> HttpResponse:
    if not request.user.can_pay(CAPSULE_PRICE):
        raise Http404('No coins!')
    return render(request, template_name='coins/collect_capsule_page.html')


@login_required
def secret_capsule(request: HttpRequest) -> HttpResponse:
    if not request.user.can_pay(CAPSULE_PRICE):
        raise Http404('No coins!')
    return render(request, template_name='coins/secret_capsule_page.html')


@require_http_methods(("GET",))
@login_required
def secret_capsule_open(request: HttpRequest) -> HttpResponse:
    user = request.user
    if not user.can_pay(CAPSULE_PRICE):
        raise Http404('No coins!')
    toy = user.get_toy_possible_2purchase()
    if toy is None:
        raise Http404('No toys to spend your gold.')
    user.buy_toy(toy, coins_payed=CAPSULE_PRICE)

    return redirect(toy.get_url())
