from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name="login"),
    path('user/<username>/', views.profile, name='profile'),
    path('logout/', views.logout_view, name="logout"),
    path('journals/create/', views.JournalCreate.as_view(), name='journals_create'),
    path('journals/<int:pk>/update/', views.JournalUpdate.as_view(), name='journals_update'),
    path('journals/<int:pk>/delete/', views.JournalDelete.as_view(), name='journals_delete'),
    path('journals/<int:journal_id>/', views.journals_show, name='journals_show'),
    path('entries/<int:entry_id>', views.entries_show, name='entries_show'),
    #entry create form route
    path('journals/<int:journal_id>/entry/create/', views.entry_create, name='entry_create'),
    path('journals/entries', views.assoc_journal_entry, name='assoc_journal_entry'),
    #entry update and delete route
    path('entries/<int:pk>/update/', views.EntryUpdate.as_view(), name='entry_update'),
    path('entries/<int:pk>/delete/', views.EntryDelete.as_view(), name='entry_delete'),

    #note create form route
    path('entry/<int:entry_id>/note/create/', views.note_create, name='note_create'),
    path('entries/notes', views.assoc_entry_note, name='assoc_entry_note'),

    #note update and delete routes
    path('notes/<int:pk>/update/', views.NoteUpdate.as_view(), name='note_update'),
    path('notes/<int:pk>/delete/', views.NoteDelete.as_view(), name='note_delete'),

    #encounter create form route
    path('entry/<int:entry_id>/encounter/create/', views.encounter_create, name='encounter_create'),
    path('entries/encounters', views.assoc_entry_encounter, name='assoc_entry_encounter'),

    #encounter update and delete routes
    path('encounterss/<int:pk>/update/', views.EncounterUpdate.as_view(), name='encounter_update'),
    path('encounters/<int:pk>/delete/', views.EncounterDelete.as_view(), name='encounter_delete'),
]