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
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Item

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
    
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class BucketView(LoginRequiredMixin, View):
    def get(self, request, bucket_id):
        try:
            bucket = Bucket.objects.get(id=bucket_id, user=request.user)
        except Bucket.DoesNotExist:
            return HttpResponse("Bucket not found", status=404)

        return render(request, 'bucket.html', {
            'bucket': bucket,
            'items': bucket.items.order_by('priority'),
        })

    def post(self, request, bucket_id):
        name = request.POST.get('name')
        quantity = request.POST.get('quantity') or 0
        price = request.POST.get('price') or 0.0

        try:
            bucket = Bucket.objects.get(id=bucket_id, user=request.user)
        except Bucket.DoesNotExist:
            return HttpResponse("Bucket not found", status=404)

        if name:
            Item.objects.create(
                name=name,
                bucket=bucket,
                quantity=int(quantity),
                price=float(price)
            )

        return redirect('bucket', bucket_id=bucket_id)

    
@csrf_exempt
def update_priority(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        for item_data in data['order']:
            Item.objects.filter(id=item_data['id']).update(priority=item_data['priority'])
        return JsonResponse({'status': 'ok'})

