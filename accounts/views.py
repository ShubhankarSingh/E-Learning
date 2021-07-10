from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import UserPassesTestMixin

from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

from django.apps import apps
model = apps.get_model('courses', 'CourseRegistration')

from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.

class SignUpView(UserPassesTestMixin, CreateView):
    form_class = CreateUserForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')
    def test_func(self):
        return self.request.user.is_anonymous
    

@login_required
def profile(request, pk=None):
    Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('accounts:account_settings')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

        all_courses = model.objects.filter(user=request.user)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'all_courses': all_courses
    }
    return render(request, 'accounts/profile.html', context)


def registered_courses(request, pk=None):
    Profile.objects.get_or_create(user=request.user)
    all_courses = model.objects.filter(user=request.user)

    context = {
        'all_courses': all_courses
    }
    return render(request, 'accounts/course_registered.html', context)
