from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login , logout
from .forms import HelpForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import HellpDesk
from django.urls import reverse

# Create your views here.
def login_view(request):
    if request.method == 'POST':     
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('all_problem')
            else:
                return render(request, 'login.html', {'error_message': 'Invalid login'})
    else:
        return render(request, 'login.html')  

def logout_user(request):
    logout(request)
    return redirect('/')


def add_problem(request):
    if request.method == 'POST':
        form = HelpForm(request.POST)
        if form.is_valid():
            help = form.save(commit=False)
            help.creator_name = request.user.username
            help.created_date = timezone.now()
            help.save()
            return redirect('thankyou')
    else:
        form = HelpForm()

    return render(request, 'help_list.html', {'form': form}) 


@login_required
def all_problems(request):
    problem = HellpDesk.objects.all()


    return render(request, 'all_problem.html', {'problems': problem })

def more_details(request, problem_id):
    problem_more = get_object_or_404(HellpDesk, pk=problem_id)
    
    if request.method == 'POST':
        actions = request.POST.get('actions', '')
        new_status = request.POST.get('status', '')

        problem_more.actions_taken = actions
        problem_more.status = new_status

        if new_status == "resolved":
            problem_more.delete()
            return redirect('all_problem')

        problem_more.save()

        return redirect(reverse('all_problem'))

    return render(request, 'more.html', {'problem_more': problem_more})

def thankyou(request):
    return render(request, "thankyou.html")
