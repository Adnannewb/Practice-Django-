from django.shortcuts import render,redirect,get_object_or_404
from .forms import SignUpForm,UserProfileForm,EventForm,RegistrationForm
from .models import UserProfile,Event,Registration,Category
from django.contrib.auth.models import User
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.urls import reverse_lazy,reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.

class Home(ListView):
    model=Event
    template_name='home.html'
    context_object_name='events'
    
class EventDetailView(DetailView):
    model=Event
    template_name='event_detail.html'
    context_object_name='event'
    
class AddEvent(LoginRequiredMixin,CreateView):
    model=Event
    form_class=EventForm
    template_name='event_form.html'
    success_url=reverse_lazy('dashboard')
    def form_valid(self, form):
        form.instance.organizer=self.request.user
        return super().form_valid(form)
    
class UpdateEvent(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Event
    form_class=EventForm
    template_name='event_form.html'
    def get_success_url(self):
        return reverse('event_detail',kwargs={'pk':self.object.pk})
    def test_func(self):
        return self.get_object().organizer==self.request.user
    

class DeleteEvent(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Event
    template_name='delete_event.html'
    def get_success_url(self):
        return reverse('dashboard')
    def test_func(self):
        return self.get_object().organizer==self.request.user

class SignUpView(CreateView):
    model=User
    form_class=SignUpForm
    template_name='signup.html'
    success_url=reverse_lazy('dashboard')
    def form_valid(self, form):
        user=form.save()
        login(self.request,user)
        return super().form_valid(form)
    
    
class UserLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True 

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'  # Replace with your actual template path

    def get_context_data(self, **kwargs):
        # 1. Fetch the default context dictionary
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # 2. Query events organized by the logged-in user
        # (Assumes your Event model has an 'organizer' foreign key to User)
        context['events'] = Event.objects.filter(organizer=user).order_by('-date')

        # 3. Query event registrations made by the logged-in user
        # (Assumes your Registration model has a 'user' foreign key)
        context['registrations'] = Registration.objects.filter(user=user).select_related('event')

        return context
class UserProfileView(LoginRequiredMixin,UpdateView):
    template_name='update_profile.html'
    model=UserProfile
    form_class=UserProfileForm
    def get_success_url(self):
        return reverse('dashboard')
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)

class EventRegister(LoginRequiredMixin,CreateView):
    model=Registration
    form_class=RegistrationForm
    template_name='event_registration.html'
    success_url=reverse_lazy('dashboard')
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    
def cancel_registration(request,pk):
    registration=get_object_or_404(Registration,pk=pk)
    if request.method=='POST' and registration.user==request.user:
        registration.status=Registration.Status.CANCELLED
        registration.save()
        return redirect('dashboard')
    return render(request,'dashboard.html',{"registration":registration})
    
    
    