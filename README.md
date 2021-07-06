# CompendDM 

## Table of Contents
* [General Info](#general-info) ℹ️
* [User Stories](#user-stories) ❔
* [Process Work](#process-work) 🤔
* [Known Issues](#known-issues) 🧐
* [Future Considerations](#future-considerations)🔮
* [Tech Stack](#tech-stack) 📚
* [Set Up](#set-up) 🎬
* [Status](#status) ⌛️


## General Info
CompenDM is a django app to take the place of pen and paper campaign journals. It's goal is to let users add notes to their journal for each campaign session, mark down monster and NPC encounters, track magic item usage and even add items to a specific players wishlist.

[Visit Live Site](https://compendm.herokuapp.com/)

## User Stories
* As a User I want to keep notes of each campaign session.
* As a User I want to keep track of monster/NPC encounters.
* As a User I want to keep track of how many days before they can use a magic item again.
* As a User I wants to add cool items that I want to someday have to a wishlist.

## Process Work
1. Established data needs for backend.
2. Set up front end and back end applications in django and built basic Journal class. Migrated Journal class to test conection between front and backend.
3. Set up login, signup and logout views, templates and urls for user so a user can start creating Journals.
4. Created protected views to all CRUD functions for Journal and Entry models. Set up urls and templates. Tested Journal CRUD and routes.
5. Added Note model, urls, views and template. Tested CRUD routes.
6. Refactored create forms for Entry and Note models to pass id of association down so users don't have to search for their entry/note on forms; it autofills.
7. Added styling.
8. Updated successful_url redirects.
9. Created an Encounters Model, views, urls, templates and forms and refactored styling for better UX.

### ERD for data needs
![ERD Screenshot](main_app/static/assets/compenDM-ERD.png)

### Screenshots of App

#### Homepage
![homepage](main_app/static/assets/homepage.png)

#### Journal Show Page
![logPage](main_app/static/assets/log-page.png)

#### Entry Show Page
![entryPage](main_app/static/assets/entryPage.png)

## Known Issues
Although associations were made on the building of each model, django forms, when using the django Create/Edit/DeleteModel templates, have no idea which user is using them or which associated model the current model's form belongs to. On testing that meant every time a user wanted to add an entry to a journal or add a note to an entry they were required to look through a dropdown (that contained every journal or entry in the database), and select the corresponding Model in order to submit a form. Not only was that incredibly cumbersome to the user it also opened up private user data to any logged in user. 

The resolution was creating my own forms, which included the associated model in the url and passing that into the form as a hidden field so the user didn't have to search the database for it. The data from that form was then passed through an association function that parsed through the data, refactored it into key/value pairs and then set that data into the newly created model before saving it to the database.

### Code Snippet
```python
# FUNCTION TO PARSE FORM DATA

def parse_data(data):
    product = {}
    if 'csrfmiddlewaretoken' in data[0]:
        product['csrfmiddlewaretoken'] = data[0].split('=')[1]
        data.pop(0)
    for item in data:
        print('( item )', item)

        if '+' in item:
            new_key = item.split('=')[0]
            words = item.split('=')[1].split('+')
            new_words = (' ').join(words)
            product[new_key] = new_words
        else:
            new_key = item.split('=')[0]
            new_value = item.split('=')[1]
            product[new_key] = new_value

    return product

# FUNCTION TO CREATE ASSOCIATION BETWEEN JOURNAL AND ENTRY MODELS
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
```

Additional known issues are: 
1. the redirect on delete paths. At the moment they redirect the user back to homepage which requires a lot of clicks to get back to where they were. Also,
2. there are some issues with the footer and background image either not covering the whole page or overlapping other info that will need to be resolved.

## Future Considerations
- Build out a search field which filters for the User to find information in their journals quickly.
- Implement a share button where a User can send entries from a journal to party members that may have missed a session so they are up to date on their notes.
- A possible rebuild in a MERN stack to make this app more functional in a live-play setting.

## Tech Stack
- django
- Bootstrap v5.0

## Set Up
1. Fork and Clone this respository to your local machine
2. In settings.py set up your backend database, create a secret key and comment out the production values for SECRET_KEY, DATABASES & ALLOWED_HOST.
3. Make migrations and migrate models to django backend.
4. Open the directory in your text editor of choice to view.

## Status
In Progress 👩🏽‍💻