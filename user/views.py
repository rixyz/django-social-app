from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, DetailView, UpdateView
from django.urls import reverse_lazy

from .models import User
from .forms import RegistrationForm, UserUpdateForm

class UserRegisterView(CreateView):
    
    template_name = 'user/register.html'
    success_url = reverse_lazy('login')
    form_class = RegistrationForm

class UserLoginView(LoginView):
    template_name = 'user/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('login')
    
    def get_success_url(self):
        return reverse_lazy('home') 
    
class ProfileView(DetailView):
    model = User
    template_name = 'user/profile.html'
    context_object_name = 'targetUser'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.post_set.all().order_by('-created_at')
        return context

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'user/edit.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})