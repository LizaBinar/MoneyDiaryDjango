from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from profiles.forms import ProfileFrom
from profiles.models import Profile


class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'profile/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        users = Profile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context['page_user'] = page_user
        return context


class CreateProfilePageView(CreateView):
    model = Profile

    template_name = 'profile/create_profile.html'
    fields = ['profile_pic', 'bio', 'facebook', 'twitter', 'instagram']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy('tasks')


class ProfileUpdateView(UpdateView):
    model = Profile
    # fields = ['profile_pic', 'bio', 'facebook', 'twitter', 'instagram']
    template_name = 'profile/update_profile.html'
    success_url = reverse_lazy('transactions_home')
    form_class = ProfileFrom
