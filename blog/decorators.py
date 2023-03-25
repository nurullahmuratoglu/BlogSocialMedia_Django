from django.http import HttpResponseBadRequest
from django.shortcuts import reverse, HttpResponseRedirect

def anonymous_required(func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('post_list'))
        return func(request, *args, **kwargs)
    return wrap