from django.shortcuts import render, redirect
from .models import UserProfile, Notes
from django.contrib.auth.hashers import make_password, check_password

def index(request):
    if request.method == 'POST':
        if 'signin' in request.POST:
            email = request.POST.get('signin-email')
            password = request.POST.get('signin-password')

            try:
                user = UserProfile.objects.get(email=email)
                if check_password(password, user.password):
                    request.session['email'] = email  # Set email in session
                    return redirect('dashboard')  # Redirect to dashboard after sign in
                else:
                    return render(request, 'index.html', {'error': 'Invalid email or password'})
            except UserProfile.DoesNotExist:
                return render(request, 'index.html', {'error': 'Invalid email or password'})

        elif 'signup' in request.POST:
            email = request.POST.get('signup-email')
            username = request.POST.get('signup-username')
            password = request.POST.get('signup-password')

            if UserProfile.objects.filter(email=email).exists():
                return render(request, 'index.html', {'error': 'Email already exists'})

            # Create user
            user = UserProfile(username=username, email=email)
            user.password = make_password(password)  # Save the hashed password
            user.save()

            # Authenticate and log in
            request.session['email'] = email  # Set email in session
            return redirect('dashboard')  # Redirect to dashboard after sign up

    return render(request, 'index.html')


def dashboard(request):
    email = request.session.get('email')
    if not email:
        return redirect('index')  # Redirect to index if user is not logged in

    user = UserProfile.objects.get(email=email)

    if request.method == 'POST':
        note_id = request.POST.get('note-id')
        title = request.POST.get('note-title')
        content = request.POST.get('note-content')

        if note_id:
            # Update existing note
            note = Notes.objects.get(id=note_id, useremail=user)
            note.title = title
            note.content = content
            note.save()
        else:
            # Create a new note
            Notes.objects.create(useremail=user, title=title, content=content)

    # Fetch the existing notes for rendering the dashboard
    notes = Notes.objects.filter(useremail=user)
    message = 'Please create a note' if not notes else None

    return render(request, 'dashboard.html', {'email': email, 'notes': notes, 'message': message})


def delete_note(request, note_id):
    if request.method == 'DELETE':
        email = request.session.get('email')
        if email:
            user = UserProfile.objects.get(email=email)
            note = Notes.objects.get(id=note_id, useremail=user)
            note.delete()
    return redirect('dashboard')


def logout(request):
    if 'email' in request.session:
        del request.session['email']
    return redirect('index')
