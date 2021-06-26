from django.shortcuts import render, redirect
from .models import Journal, Entry
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView


# Create your views here.

#function to render user's profile page // login required
@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    journals = Journal.objects.filter(user=user)
    return render(request, 'profile.html', {'username': username, 'journals': journals})

# Function to render index page // App Home page - not protected
def index(request):
    return render(request, 'index.html')

#Function to render login page
def login_view(request):
# if post, then authenticate (user submitted username and password)
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/user/'+u)
                else:
                    print('The account has been disabled.')
                    return HttpResponseRedirect('/')
        else:
            print('The username and/or password is incorrect.')
            return HttpResponseRedirect('/login')
    else: # it was a get request so send the emtpy login form
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})
#function that logouts user and redirects them back to the app homepage
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

#function to render signup page
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # print(help(form))
        if form.is_valid():
            user = form.save()
            u = form.cleaned_data['username']
            login(request, user)
            return redirect('/user/'+ u)
            # return redirect('/')
        else:
            print('Invalid form submitted')
            return redirect('/signup')
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form })

# CRUD FOR JOURNAL MODEL

def journals_index(request):
    journals = Journal.objects.all()
    data = { 'journals': journals }
    return render(request, 'journals/index.html', data)

def journals_show(request, journal_id):
    journal = Journal.objects.get(id=journal_id)
    entries = Entry.objects.all()
    data = { 
        'journal': journal,
        'entries': entries }
    return render(request, 'journals/show.html', data)

# forms - generic from django
@method_decorator(login_required, name='dispatch')
class JournalCreate(CreateView):
    model = Journal
    fields = ['title']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect('/journals/' + str(self.object.pk))
        
@method_decorator(login_required, name='dispatch')
class JournalUpdate(UpdateView):
    model = Journal
    fields = ['title']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect('/journals/' + str(self.object.pk))

@method_decorator(login_required, name='dispatch')
class JournalDelete(DeleteView):
    model = Journal
    success_url = '/'

# CRUD FOR ENTRY MODEL

def entries_show(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    return render(request, 'entries/show.html', {'entry': entry})

class EntryCreate(CreateView):
    model = Entry
    fields = '__all__'
    success_url = '/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect('/')

class EntryUpdate(UpdateView):
    model = Entry
    fields = ['name', 'date']
    success_url = '/'

class EntryDelete(DeleteView):
    model = Entry
    success_url = '/'