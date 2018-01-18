"""
    @author @pdonaire1
    Pablo Gonzlez Donaire
"""
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic import FormView, RedirectView
from .forms import LoginForm
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from rentals.models import Rental
from django.contrib.auth.mixins import LoginRequiredMixin

class Index(LoginRequiredMixin, TemplateView):
    """!
    Clase de la vista inicial

    @author @pdonaire1
    Pablo Gonzalez Donaire
    """
    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rentals'] = Rental.objects.all()
        return context

class LoginView(FormView):
    """
    View that make the login of the platform
    """
    form_class = LoginForm
    template_name = 'user.login.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        """
        Method that validate the form
        """
        usuario = form.cleaned_data['usuario']
        contrasena = form.cleaned_data['contrasena']
        usuario = authenticate(username=usuario, password=contrasena)
        if usuario.is_superuser or User.objects.filter(pk=usuario.id, groups__name='Administrador').exists():
            login(self.request, usuario)
            if self.request.POST.get('remember_me') is not None:
                # Session expira a los dos meses si no se deslogea
                self.request.session.set_expiry(1209600)
        return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):
    """
    Class to logout the user
    """
    permanent = False
    query_string = True

    def get_redirect_url(self):
        """!
        Redirect to client to index
        """
        logout(self.request)
        return reverse_lazy('index')
