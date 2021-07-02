from django.shortcuts import render, redirect
from .models import Encounter, Journal, Entry, Note
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


# VIEWS

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

# SHOWS ALL JOURNALS
def journals_index(request):
    journals = Journal.objects.all()
    data = { 'journals': journals }
    return render(request, 'journals/index.html', data)

#SHOWS SPECIFIC JOURNAL
def journals_show(request, journal_id):
    journal = Journal.objects.get(id=journal_id)
    entries = Entry.objects.filter(journal=journal_id)
    data = { 
        'journal': journal,
        'entries': entries }
    return render(request, 'journals/show.html', data)

# forms - generic from django // CREATES NEW JOURNAL
@method_decorator(login_required, name='dispatch')
class JournalCreate(CreateView):
    model = Journal
    fields = ['title']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect('/journals/' + str(self.object.pk))

#UPDATES JOURNAL
@method_decorator(login_required, name='dispatch')
class JournalUpdate(UpdateView):
    model = Journal
    fields = ['title']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect('/journals/' + str(self.object.pk))

#DELETES JOURNAL
@method_decorator(login_required, name='dispatch')
class JournalDelete(DeleteView):
    model = Journal
    success_url = '/'


#~~~~~~~~~~~~~~~~~~#

# CRUD FOR ENTRY MODEL

#SHOWS SPECIFIC ENTRY
def entries_show(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    notes = Note.objects.filter(entry=entry)
    encounters = Encounter.objects.filter(entry=entry)
    return render(request, 'entries/show.html', {'entry': entry, 'notes': notes, 'encounters': encounters})

#UPDATES SPECIFIC ENTRY
@method_decorator(login_required, name='dispatch')
class EntryUpdate(UpdateView):
    model = Entry
    fields = ['name', 'date']
    # success_url = '/'
    
    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect('/entries/' + str(self.object.pk))

#DELETES SPECIFIC ENTRY
@method_decorator(login_required, name='dispatch')
class EntryDelete(DeleteView):
    model = Entry
    success_url = '/'

#~~~~~~~~~~~~~~~#

# function to parse form data

def parse_data(data):
    product = {}
    if 'csrfmiddlewaretoken' in data[0]:
        product['csrfmiddlewaretoken'] = data[0].split('=')[1]
        data.pop(0)
        # print('( new data )', data)
    # print('( woah MULE )')
    for item in data:
        # print('( item )', item)
        # new_phrase = None
        if '+' in item:
            new_key = item.split('=')[0]
            words = item.split('=')[1].split('+')
            new_words = (' ').join(words)
            # print('( final phase )', new_words)
            product[new_key] = new_words
        else:
            new_key = item.split('=')[0]
            new_value = item.split('=')[1]
            product[new_key] = new_value

    return product

#~~~~~~~~~~~~~~~~~#

# CREATE ENTRY VIEW

def entry_create(request, journal_id):
    journal = Journal.objects.get(id=journal_id)
    user = request.user

    return render(request, 'createEntry.html', { 'journal': journal, 'user': user })


#FUNCTION TO ESTABLISH ASSOCIATION BETWEEN JOURNAL AND ENTRY MODELS
def assoc_journal_entry(request):
    split_form_data = str(request.body).split('&')
    x = parse_data(split_form_data)
    new_journal = int(x.get('journal').split("'")[0]) 
    x['journal'] = new_journal

    e = Entry(
        name=x.get('name'),
        date=x.get('date'),
        journal_id=x.get('journal')
    )
    e.save()

    return HttpResponseRedirect('/journals/' + str(new_journal))


#CRUD ROUTES FOR NOTE MODEL

#CREATE NOTE VIEW

def note_create(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    user = request.user

    return render(request, 'createNote.html', { 'entry': entry, 'user': user })

#FUNCTION TO ESTABLISH ASSOCIATION BETWEEN ENTRY AND NOTE MODELS
def assoc_entry_note(request):
    split_form_data = str(request.body).split('&')
    x = parse_data(split_form_data)
    new_entry = int(x.get('entry').split("'")[0])
    x['entry'] = new_entry

    n = Note(
        content=x.get('content'),
        entry_id=x.get('entry')
    )
    n.save()

    return HttpResponseRedirect('/entries/' + str(new_entry))

#UPDATES SPECIFIC NOTE
@method_decorator(login_required, name='dispatch')
class NoteUpdate(UpdateView):
    model = Note
    fields = ['content']

    def form_valid(self, form):
        form.save()
        entry = Entry.objects.get(id=self.object.entry_id)
        # print(entry.id)
        return HttpResponseRedirect('/entries/' + str(entry.id))

#DELETES SPECIFIC NOTE
@method_decorator(login_required, name='dispatch')
class NoteDelete(DeleteView):
    model = Note
    success_url = '/'



#CRUD ROUTES FOR ENCOUNTER MODEL

#CREATE ENCOUNTER VIEW


def encounter_create(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    user = request.user

    return render(request, 'createEncounter.html', { 'entry': entry, 'user': user })

#FUNCTION TO ESTABLISH ASSOCIATION BETWEEN ENTRY AND ENCOUNTER MODELS
def assoc_entry_encounter(request):
    split_form_data = str(request.body).split('&')
    x = parse_data(split_form_data)
    new_entry = int(x.get('entry').split("'")[0])
    x['entry'] = new_entry

    enc = Encounter(
        name=x.get('name'),
        entry_id=x.get('entry')
    )
    enc.save()

    return HttpResponseRedirect('/entries/' + str(new_entry))

#UPDATES SPECIFIC Encounter
@method_decorator(login_required, name='dispatch')
class EncounterUpdate(UpdateView):
    model = Encounter
    fields = ['content']

    def form_valid(self, form):
        form.save()
        entry = Entry.objects.get(id=self.object.entry_id)
        # print(entry.id)
        return HttpResponseRedirect('/entries/' + str(entry.id))

#DELETES SPECIFIC Encounter
@method_decorator(login_required, name='dispatch')
class EncounterDelete(DeleteView):
    model = Encounter
    success_url = '/'
