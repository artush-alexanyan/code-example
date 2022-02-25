from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.views.decorators.http import require_http_methods
from auth2.models import User
from gift.models import Gift
from toy.models import ToyPage, put_to_collection, ToyCollection, is_already_collected
from django.core.exceptions import ValidationError


@require_http_methods(["GET", ])
@login_required
def apply_code(request, code):
    user = request.user
    try:
        code_obj = Gift.objects.get(code=code)
    except Gift.DoesNotExist:
        raise Http404('Invalid code')
    if not code_obj.is_active():
        raise Http404('Code already used')
    toy = code_obj.toy
    if is_already_collected(toy, user):
        raise Http404('You have already collected a promotional toy')
    if code_obj.allow_ignore_quota:
        pass
    elif toy.is_limit_reached():
        raise Http404('All toys collected, limit reached')

    user.gift(toy, force=True)
    ToyCollection.upgrade_collection(toy, user)
    code_obj.redeemed = code_obj.redeemed + 1
    code_obj.user = user
    code_obj.save()
    return redirect(toy.get_url())
