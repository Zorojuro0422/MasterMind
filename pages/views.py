from pyexpat.errors import messages
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from .models import Accounts, Group, ChatMessage, SharedNote
from .models import Flashcard, CreateFlashcard, Notes, CompilerSubmission
from django.contrib import messages
from django.shortcuts import redirect
from .models import SharedFlashcard
import html
import os
import io
import sys


def home(request):

    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
 
        # Client-side validation is handled by JavaScript, so no need to check it here
 
        # Proceed with saving data to the database
        obj = Accounts()
        obj.email = email
        obj.username = username
        obj.password = password
        obj.save()
       
        # Redirect to the login page after successful registration
        return redirect('login')  # Replace 'login' with the actual URL name for your login page
 
    context = {}
 
    return render(request, 'pages/home.html', context)
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Check if the user exists in the database
        user = Accounts.objects.filter(email=email, password=password).first()
        if user:
            # Password is correct, log in the user
            request.session['user_email'] = email

            # Get the user's information
            user_info = {
                'username': user.username,
                'profile_picture': user.profile_picture.url if user.profile_picture else 'default-profile.png'
            }

            return render(request, 'pages/main.html', {'user_info': user_info})

        return render(request, 'pages/login.html', {'login_failed': True})

    return render(request, 'pages/login.html')

def logout(request):
    print("Entering logout view")
    if 'user_email' in request.session:
        del request.session['user_email']
        print("User logged out successfully")
    else:
        print("User is not logged in")
    return redirect('login')
        
def landingpage(request):
    context ={
    }
    return render(request,'pages/landingpage.html', context)

def main(request):
    if 'user_email' in request.session:
        # Retrieve the user based on the email
        user_email = request.session['user_email']
        user = Accounts.objects.get(email=user_email)

        # Retrieve the groups associated with the logged-in user
        groups = Group.objects.filter(group_members=user)

        # Pass the groups queryset to the template context
        context = {'groups': groups}
        return render(request, 'pages/main.html', context)
    else:
        # Handle the case where the user is not logged in
        return redirect('login')
    
def profile(request):
    return render(request,'pages/profile.html')

def flashcard(request):
    if 'user_email' in request.session:
        user_email = request.session['user_email']

        # Retrieve the user based on the email
        user = Accounts.objects.get(email=user_email)

        if request.method == 'POST':
            title = request.POST.get('title')

            # Check if a flashcard with the same title already exists for this user
            if not Flashcard.objects.filter(title=title, user=user).exists():
                # Create a new flashcard associated with the logged-in user
                flashcard_obj = Flashcard(title=title, user=user)
                flashcard_obj.save()

            # Redirect to the 'createflashcard' page after processing the POST request
            return redirect('createflashcard', flashcard_title=title)

        # Retrieve flashcards associated with the logged-in user
        flashcards = Flashcard.objects.filter(user=user)

        # Pass the flashcards queryset to the template
        context = {'flashcards': flashcards}

        # Render the 'pages/flashcard.html' template for GET requests
        return render(request, 'pages/flashcard.html', context)
    else:
        # Handle the case where the user is not logged in
        return redirect('login')

# NOTES FEATURE
def notes(request):
    if 'user_email' in request.session:
        user_email = request.session['user_email']

        # Retrieve the user based on the email
        user = Accounts.objects.get(email=user_email)

        # Retrieve all notes associated with the logged-in user
        notes = Notes.objects.filter(user=user)

        context = {'notes': notes}
        return render(request, 'pages/note.html', context)
    else:
        # Handle the case where the user is not logged in
        return redirect('login')

def createnote(request):
    if request.method == 'POST':
        content = request.POST.get('content')  # Make sure 'definition' is present in your form data
        title = request.POST.get('title')

        # Create an instance of CreateFlashcard associated with the flashcard
        note_obj = Notes(title=title, content=content)
        note_obj.save()

        # Add a success message
        messages.success(request, 'Note saved successfully.')

        # Redirect back to the notes.html page
        return redirect('note')

    # Pass the flashcards queryset to the template
    context = {'notes': notes}

    # Render the 'pages/flashcard.html' template for GET requests
    return render(request, 'pages/createnote.html', context)

def displaynote(request):
    title = request.GET.get('title')
    notes = get_object_or_404(Notes, title=title)
    
    # Filter CreateFlashcard objects based on the associated flashcard
    create_note = Notes.objects.filter(title=title)
    
    # Retrieve and format the definitions and terms
    content = [html.unescape(notes.content.strip()) for note in create_note]
    title = [html.unescape(notes.title.strip()) for note in create_note]

    if request.method == "POST":
        #Delete currently selected note
        notes.delete()

        # Redirect back to the notes.html page
        return redirect('note')

        # Add a success message
        messages.success(request, 'Note deleted successfully.')

    context = {
        'notes': notes
    }

    return render(request, 'pages/displaynote.html', context)

def editnote(request, title):
    # Retrieve the note with the specified title
    note = get_object_or_404(Notes, title=title)

    if request.method == 'POST':
        new_content = request.POST.get('content')
        new_title = request.POST.get('title')

        note.content = new_content
        note.title = new_title
        note.save()

        # Redirect back to the displaynote.html page
        return redirect('note')

    context = {'note': note}
    return render(request, 'pages/editnote.html', context)
#FLASHCARD FEATURE
def createflashcard(request, flashcard_title):
    # Retrieve the specific flashcard based on the title
    flashcard = get_object_or_404(Flashcard, title=flashcard_title)

    if request.method == 'POST':
        definition = request.POST.get('definition')
        term = request.POST.get('term')

        # Create an instance of CreateFlashcard associated with the flashcard
        create_flashcard_obj = CreateFlashcard(flashcard=flashcard, difinition=definition, term=term)
        create_flashcard_obj.save()

        # Redirect back to the flashcard detail page
        return redirect('createflashcard', flashcard_title=flashcard_title)

    # If it's a GET request, you can render the form or provide any necessary context
    context = {'flashcard': flashcard}
    return render(request, 'pages/createflashcard.html', context)

def displayflashcard(request):
    title = request.GET.get('title')
    flashcard = get_object_or_404(Flashcard, title=title)
    
    # Filter CreateFlashcard objects based on the associated flashcard
    create_flashcards = CreateFlashcard.objects.filter(flashcard=flashcard)
    
    # Retrieve and format the definitions and terms
    definitions = [html.unescape(flashcard.difinition.strip()) for flashcard in create_flashcards]
    terms = [html.unescape(flashcard.term.strip()) for flashcard in create_flashcards]

    context = {
    'flashcard': flashcard,
    'flashcard_id': flashcard.title,  # Use the ID of the flashcard
    'definitions': definitions,
    'terms': terms,
    'num_flashcards': len(create_flashcards),
}

    return render(request, 'pages/displayflashcard.html', context)

def edit_flashcard(request, flashcard_id):
    # Retrieve all flashcards for the given flashcard_id
    flashcards = CreateFlashcard.objects.filter(flashcard_id=flashcard_id)

    if request.method == 'POST':
        # Handle form submission to update flashcard data
        # Use a loop to go through each flashcard and update its definition and term
        for flashcard in flashcards:
            new_definition = request.POST.get(f'definition_{flashcard.id}')
            new_term = request.POST.get(f'term_{flashcard.id}')

            flashcard.difinition = new_definition
            flashcard.term = new_term
            flashcard.save()

        # Redirect back to the displayflashcard.html page
        return redirect('flashcard')

    context = {'flashcards': flashcards}
    return render(request, 'pages/edit_flashcard.html', context)

def delete_flashcard(request, flashcard_id):
    # Retrieve all flashcards for the given flashcard_id
    flashcards = CreateFlashcard.objects.filter(flashcard_id=flashcard_id)

    if request.method == 'POST':
        # Process the deletion of flashcards that are selected
        for flashcard in flashcards:
            # Check if this flashcard is selected for deletion
            delete_key = f'delete_{flashcard.id}'
            if delete_key in request.POST:
                flashcard.delete()

        # Add a success message
        messages.success(request, 'Flashcards deleted successfully.')

        # Redirect back to the displayflashcard.html page
        return redirect('flashcard')

    context = {'flashcards': flashcards}
    return render(request, 'pages/delete_flashcard.html', context)

def quiz(request):
    if 'user_email' in request.session:
        user_email = request.session['user_email']

        # Retrieve the user based on the email
        user = Accounts.objects.get(email=user_email)

        # Retrieve all flashcards associated with the logged-in user
        flashcards = Flashcard.objects.filter(user=user)

        if request.method == 'POST':
            title = request.POST.get('title')

            # Check if a flashcard with the same title already exists for this user
            if not Flashcard.objects.filter(title=title, user=user).exists():
                # Create a new flashcard associated with the logged-in user
                flashcard_obj = Flashcard(title=title, user=user)
                flashcard_obj.save()

            # Redirect to the 'createflashcard' page after processing the POST request
            return redirect('createflashcard', flashcard_title=title)

        # Pass the flashcards queryset to the template
        context = {'flashcards': flashcards}

        # Render the 'quiz.html' template with the context data
        return render(request, 'pages/quiz.html', context)
    else:
        # Handle the case where the user is not logged in
        return redirect('login')
    
def takequiz(request):
    title = request.GET.get('title')
    flashcard = get_object_or_404(Flashcard, title=title)
    
    # Filter CreateFlashcard objects based on the associated flashcard
    create_flashcards = CreateFlashcard.objects.filter(flashcard=flashcard)
    
    # Retrieve and format the definitions and terms
    definitions = [html.unescape(flashcard.difinition.strip()) for flashcard in create_flashcards]
    terms = [html.unescape(flashcard.term.strip()) for flashcard in create_flashcards]

    context = {
    'flashcard': flashcard,
    'flashcard_title': flashcard.title,  # Use the ID of the flashcard
    'definitions': definitions,
    'terms': terms,
    'num_flashcards': len(create_flashcards),
}
    return render (request, 'pages/takequiz.html', context)

def creategroup(request):
    context ={
    }
    return render(request,'pages/creategroup.html', context)

def addgroup(request):
    if 'user_email' in request.session:
        if request.method == 'POST':
            group_title = request.POST.get('group_title')
            if group_title:
                member_emails = request.POST.get('members').split(',')

                # Create a new group
                group = Group(group_title=group_title)
                group.save()

                # Add the user who is creating the group to the group
               # user_email = request.session['user_email']
               # try:
              #      user = Accounts.objects.get(email=user_email)
              #      group.group_members.add(user)
               # except Accounts.DoesNotExist:
                    # Handle the case where the user doesn't exist
                    # You can add error handling or skip this user as needed

                # Add other members to the group
                for email in member_emails:
                    email = email.strip()
                    try:
                        member = Accounts.objects.get(email=email)
                        group.group_members.add(member)
                    except Accounts.DoesNotExist:
                        # Handle the case where the user doesn't exist
                        # You can add error handling or skip this user as needed

                # Redirect to a success page or group detail page
                     return redirect('group')  # Redirect to a page showing the group

        # Render the form to create a new group
        return render(request, 'pages/addgroup.html')
    else:
        # Handle the case where the user is not logged in
        return redirect('login')

def group(request, group_id):
    messages = []  # Initialize messages list

    if 'user_email' in request.session:
        try:
            group = Group.objects.get(pk=group_id)
            user_email = request.session['user_email']
            user = Accounts.objects.get(email=user_email)

            if user in group.group_members.all():
                if request.method == 'POST':
                    # Check if the request is for adding a member
                    if 'add_member_email' in request.POST:
                        add_member_email = request.POST.get('add_member_email')
                        try:
                            new_member = Accounts.objects.get(email=add_member_email)
                            group.group_members.add(new_member)
                            group.save()
                            messages.append(f"{new_member.username} added to the group successfully.")
                            return redirect('group', group_id=group.pk)

                        except Accounts.DoesNotExist:
                            messages.append(f"User with email {add_member_email} does not exist.")
                            return redirect('group', group_id=group_id)

                    # Check if the request is for removing a member by username
                    elif 'remove_member_username' in request.POST:
                        remove_member_username = request.POST.get('remove_member_username')
                        try:
                            member_to_remove = Accounts.objects.get(username=remove_member_username)
                            group.group_members.remove(member_to_remove)
                            group.save()
                            messages.append(f"{member_to_remove.username} removed from the group successfully.")
                            return redirect('group', group_id=group.pk)

                        except Accounts.DoesNotExist:
                            messages.append(f"Member with username {remove_member_username} does not exist.")
                            return redirect('group', group_id=group_id)

                    # Check if the request is for sending a message
                    elif 'message_text' in request.POST:
                        message_text = request.POST.get('message_text')
                        if message_text:
                            # Save the message to the database
                            chat_message = ChatMessage(group=group, sender=user, message=message_text)
                            chat_message.save()

                            # Redirect back to the group's chat page
                            return redirect('group', group_id=group.pk)

                # Retrieve the members of the group
                group_members = group.group_members.all()

                # Retrieve the chat messages for the group
                messages = ChatMessage.objects.filter(group=group)

                # Retrieve shared flashcards for the group
                shared_flashcards = SharedFlashcard.objects.filter(group=group)

                shared_notes = SharedNote.objects.filter(group=group)
                

                # Pass the group, its members, messages, and shared flashcards to the template context
                context = {
                    'group': group,
                    'group_members': group_members,
                    'messages': messages,
                    'user': user,
                    'shared_flashcards': shared_flashcards,  # Add shared flashcards to the context
                    'shared_notes': shared_notes,
                }

                return render(request, 'pages/group.html', context)
            else:
                # Handle the case where the user is not a member of the group
                return redirect('group_list')  # Redirect to a group list page
        except Group.DoesNotExist:
            # Handle the case where the group doesn't exist
            return redirect('group_list')  # Redirect to a group list page
    else:
        # Handle the case where the user is not logged in
        return redirect('login')


def shareflashcard(request, group_id):
    if 'user_email' in request.session:
        user_email = request.session['user_email']
        user = Accounts.objects.get(email=user_email)

        try:
            group = Group.objects.get(pk=group_id)

            if request.method == 'POST':
                selected_flashcard_title = request.POST.get('flashcard_title')

                if selected_flashcard_title:
                    # Process the selected flashcard title
                    flashcard_to_share = Flashcard.objects.get(title=selected_flashcard_title)

                    # Share the selected flashcard with the group
                    shared_flashcard, created = SharedFlashcard.objects.get_or_create(group=group, flashcard=flashcard_to_share)

                    if created:
                        return redirect('group', group_id=group_id)
                    else:
                        return HttpResponse("Flashcard is already shared with the group.")
                else:
                    return HttpResponse("No flashcard selected. Please go back and select a flashcard.")

            else:
                # Retrieve all flashcards associated with the logged-in user
                flashcards = Flashcard.objects.filter(user=user)
                flashcard_details = [{'title': flashcard.title} for flashcard in flashcards]

                # Pass the flashcards and group to the template
                context = {'flashcard_details': flashcard_details, 'flashcards': flashcards, 'group_id': group_id, 'group': group}
                return render(request, 'pages/shareflashcard.html', context)

        except Group.DoesNotExist:
            return HttpResponse("Group not found")

    else:
        return redirect('login')
    
    TEMP_DIR = os.path.join(tempfile.gettempdir(), 'compiler_temp_files')

def compiler(request):
    if request.method == 'POST':
        code = request.POST.get('code', '')
        result = execute_code(code)
        
        # Save the submission to the database
        submission = CompilerSubmission.objects.create(code=code, result=result)
        submission.save()

        return render(request, 'pages/compiler.html', {'result': result, 'submission': submission})

    return render(request, 'pages/compiler.html', {'result': None, 'submission': None})

def execute_code(code):
    """
    Execute the provided code and capture standard output.
    """
    try:
        # Create a dictionary to store the variables for the executed code
        local_vars = {}
        
        # Redirect standard output to capture the result
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Execute the code using the exec function
        exec(code, globals(), local_vars)
        
        # Reset standard output
        sys.stdout = sys.__stdout__

        # Get the captured output
        result = captured_output.getvalue()

        return result.strip()
    
    except Exception as e:
        # Handle any exceptions that might occur during code execution
        return f"Error: {str(e)}"

def sharenote(request, group_id):
    if 'user_email' in request.session:
        user_email = request.session['user_email']
        user = Accounts.objects.get(email=user_email)  # Assuming you have an Accounts model

        try:
            group = Group.objects.get(pk=group_id)

            if request.method == 'POST':
                selected_note_titles = request.POST.getlist('note_title')

                if selected_note_titles:
                    for selected_note_title in selected_note_titles:
                        # Process each selected note title
                        try:
                            note_to_share = Notes.objects.get(title=selected_note_title)

                            # Share the selected note with the group
                            shared_note, created = SharedNote.objects.get_or_create(group=group, note=note_to_share)

                            if not created:
                                return HttpResponse(f"Note '{note_to_share.title}' is already shared with the group.")
                        except Notes.DoesNotExist:
                            return HttpResponse(f"Note '{selected_note_title}' does not exist.")
                else:
                    return HttpResponse("No note selected. Please go back and select a note.")

                return redirect('group', group_id=group_id)
            else:
                # Retrieve all notes associated with the logged-in user
                notes = Notes.objects.filter(user=user)
                note_details = [{'title': note.title} for note in notes]

                # Pass the notes and group to the template
                context = {'note_details': note_details, 'notes': notes, 'group_id': group_id, 'group': group}
                return render(request, 'pages/sharenote.html', context)

        except Group.DoesNotExist:
            return HttpResponse("Group not found")

    else:
        return redirect('login')
