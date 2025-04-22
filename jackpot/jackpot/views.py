from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm  # Django's built-in user creation form
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Bucket
from .forms import BucketForm

class Login(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('dashboard')

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()  # Instantiate an empty form
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)  # Populate form with POST data
        if form.is_valid():
            form.save()  # Save the new user
            return redirect('login')  # Redirect to login page after successful registration
        return render(request, 'register.html', {'form': form})
def index(request):
    return render(request, 'index.html')

def manager(request):
    return render(request, 'manager.html')

def settings(request):
    return render(request, 'settings.html')


class dashboard(LoginRequiredMixin, View):
    def get(self, request):
        # Get the current user's buckets
        bucket_qs = Bucket.objects.filter(user=request.user)
        bucket_list = list(bucket_qs.values('name', 'percentage'))  # 👈 JSON-serializable

        form = BucketForm()  # Initialize the form to create a new bucket

        return render(request, 'dashboard.html', {
            'username': request.user.username,
            'buckets': bucket_qs,        # for the {% for bucket in buckets %} loop
            'bucket_json': bucket_list,  # for use in JSON script
            'form': form
        })
    def post(self, request):
        form = BucketForm(request.POST)
        if form.is_valid():
            bucket = form.save(commit=False)
            bucket.user = request.user
            bucket.save()
            return redirect('dashboard')

        bucket_qs = Bucket.objects.filter(user=request.user)
        bucket_list = list(bucket_qs.values('name', 'percentage'))

        return render(request, 'dashboard.html', {
            'username': request.user.username,
            'buckets': bucket_qs,
            'bucket_json': bucket_list,
            'form': form
        })

