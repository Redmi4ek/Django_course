from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login , logout
from .forms import HelpForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import HellpDesk
from django.urls import reverse
from django.contrib.auth.models import Group, User
from django.db.models import Q


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
            reception_group = Group.objects.get(name='Reception')
            reception_users = reception_group.user_set.all()
            if reception_users:
                first_reception_user = reception_users.first()
                help.assigned_user = first_reception_user
            help.save()
            return redirect('thankyou')
    else:
        form = HelpForm()

    return render(request, 'help_list.html', {'form': form}) 


@login_required
def all_problems(request):
    reception_group = Group.objects.get(name='Reception')
    tester_group = Group.objects.get(name='Tester')
    is_reception_user = reception_group.user_set.filter(id=request.user.id).exists()
    is_tester_user = tester_group.user_set.filter(id=request.user.id).exists()

    if is_reception_user or is_tester_user:
        if is_reception_user:
            problems = HellpDesk.objects.filter(assigned_user=request.user)
        elif is_tester_user:
            problems = HellpDesk.objects.filter(Q(creator_name=request.user.username) | Q(status='resolved', confirmed=False) )
    else:
        problems = HellpDesk.objects.filter(confirmed=False)

    return render(request, 'all_problem.html', {'is_reception_user': is_reception_user, 'is_tester_user': is_tester_user, 'problems': problems })

def more_details(request, problem_id):
    problem_more = get_object_or_404(HellpDesk, pk=problem_id)
    is_tester = request.user.groups.filter(name= 'Tester')
    is_reception = request.user.groups.filter(name= 'Reception')
    reception_users = User.objects.filter(groups__name='Reception')


    if request.method == 'POST':
        actions = request.POST.get('actions', '')
        new_status = request.POST.get('status', '')
        new_assigned_user_id = request.POST.get('assigned_user', None)
        
        
        if is_tester:
            if new_status == "confirmed":
                problem_more.delete()
                return redirect('all_problem')
            else:
                problem_more.actions_taken = actions
                problem_more.status = new_status

            if new_assigned_user_id:
                new_assigned_user = User.objects.get(id=new_assigned_user_id)
                problem_more.assigned_user = new_assigned_user
                problem_more.save()

        elif is_reception:
            if new_status in ['new', 'in progress']:
                problem_more.status = new_status
                problem_more.actions_taken = actions
                
                if new_assigned_user_id:
                    new_assigned_user = User.objects.get(id=new_assigned_user_id)
                    problem_more.assigned_user = new_assigned_user
                problem_more.save()
            
            elif new_status == 'resolved' and problem_more.status != 'resolved':
                # Запрет изменения на "resolved", если статус уже "resolved"
                problem_more.status = new_status
                problem_more.assigned_user = None
                problem_more.actions_taken = actions
                problem_more.save()

        problem_more.save()

        return redirect(reverse('all_problem'))

    return render(request, 'more.html', {'problem_more': problem_more , 'is_tester' : is_tester , 'is_recepption': is_reception , 'reception_users': reception_users})

def thankyou(request):
    return render(request, "thankyou.html")
