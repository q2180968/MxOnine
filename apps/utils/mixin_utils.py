from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        request.session['red_url'] = request.path
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
