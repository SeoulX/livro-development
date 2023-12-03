from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from functools import wraps
from django.contrib.auth.hashers import make_password, check_password



def land(request):
    return render(request, 'livrowebapp/landing.html')
def signin(request):
    if request.method == "GET":
        identifier = request.GET.get('identifier')
        passw = request.GET.get('pass')
        now = datetime.now()
        hour = now.hour
        greeting = 'Good Morning' if 5 <= hour < 12 else ('Good afternoon' if 12 <= hour < 18 else 'Good Evening')
        try:
            member = Member.objects.get(Q(email=identifier) | Q(username=identifier), password=passw)
            request.session['member'] = {
                    'username': member.username,
                    'email': member.email,
                    'password' : member.password,
                    'type_user': member.type_user,
                    'about_user': member.about_user
                }
            if member.type_user == 'Reader':
                messages.success(request, f'{greeting}, {member.username}!')
                return redirect('browse_reader')
            elif member.type_user == 'Writer':
                messages.success(request, f'{greeting}, {member.username}!')
                return redirect('browse_writer')
        except Member.DoesNotExist as e:
            print(f"Error: {e}")
            return render(request, 'livrowebapp/signin.html')
    else:
        return render(request, 'livrowebapp/signin.html')
def signup(request):
    if request.method == "POST":
        usrname = request.POST.get('username')
        mail = request.POST.get('email')
        passw = request.POST.get('password')
        confirmpass = request.POST.get('confirmpass')
        if passw == confirmpass:
            form = Memberform(request.POST or None)
            if form.is_valid():
                member = form.save(commit=False)
                member.password = make_password(passw)  # Hash the password
                member.save()

                # Use check_password to verify the password
                if check_password(passw, member.password):
                    request.session['member'] = {
                        'username': member.username,
                        'email': member.email,
                        'password': member.password,
                        'type_user': member.type_user,
                        'about_user': member.about_user
                    }
                    if member.type_user == 'Reader':
                        messages.success(request, ('Thanks for Signing Up!'))
                        return redirect('browse_reader')
                    elif member.type_user == 'Writer':
                        messages.success(request, ('Thanks for Signing Up!'))
                        return redirect('browse_writer')
                else:
                    messages.error(request, ('Password Not Match!'))
        else:
            messages.error(request, ('Password Not Match!'))
    else:    
        return render(request, 'livrowebapp/signup.html')
def aboutus(request):
    return render(request, 'livrowebapp/aboutus.html')
def aboutus_logged(request):
    member_data = request.session.get('member', None)
    return render(request, 'livrowebapp/aboutus_logged.html', {'member': member_data})
def browse_reader(request):
    member_data = request.session.get('member', None)
    all_books = Book.objects.all()
    for book in all_books:
        book.genre_list = book.genre.split(', ')
    return render(request,  'livrowebapp/browse_reader.html', {'member': member_data, 'all_books': all_books})
def browse_writer(request):
    member_data = request.session.get('member', None)
    all_books = Book.objects.all()
    for book in all_books:
        book.genre_list = book.genre.split(', ')
    return render(request, 'livrowebapp/browse_writer.html', {'member': member_data, 'all_books': all_books})
def profile(request):
    member_data = request.session.get('member', None)
    return render(request, 'livrowebapp/profile.html', {'member': member_data})
def profile_writer(request):
    member_data = request.session.get('member', None)
    return render(request, 'livrowebapp/profile_writer.html', {'member': member_data})
def manageprofile(request):
    member_data = request.session.get('member', None)
    return render(request, 'livrowebapp/manageprofile.html', {'member': member_data})
def manageprofile_writer(request):
    member_data = request.session.get('member', None)
    return render(request, 'livrowebapp/manageprofile_writer.html', {'member': member_data})
def addbooks(request):
    member_data = request.session.get('member', None)
    if request.method == 'POST':
        formBook = BookForm(request.POST, request.FILES)
        if formBook.is_valid():
            book = formBook.save(commit=False)
            book.uploader = Member.objects.get(username=member_data['username'])
            book.uploader_user = member_data['username']
            book.save()
            messages.success(request, 'Book added successfully!')
            return redirect('profile_writer')
        else:
            messages.error(request, 'Error adding the book. Please check the form.')
    else:
        formBook = BookForm()
    return render(request, 'livrowebapp/addbooks.html', {'member': member_data})
def updatebooks(request):
    member_data = request.session.get('member', None)
    if member_data['type_user'] == 'Writer':
        books = Book.objects.filter(uploader_user=member_data['username'])
        return render(request, 'livrowebapp/updatebooks.html', {'member': member_data, 'books': books})
    else:
        return redirect('profile_writer')
def edit_book(request, book_id):
    member_data = request.session.get('member', None)
    if member_data['type_user'] == 'Writer':
        book = get_object_or_404(Book, id=book_id, uploader_user=member_data['username'])
        if request.method == 'POST':
            form = BookForm(request.POST, request.FILES, instance=book)
            if form.is_valid():

                updated_book = form.save(commit=False)
                

                new_cover = request.FILES.get('book_cover')
                if new_cover:
                    updated_book.book_cover = new_cover
                

                updated_book.save()

                messages.success(request, 'Book updated successfully!')
                return redirect('updatebooks')
            else:
                messages.error(request, 'Error updating the book. Please check the form.')
        else:
            form = BookForm(instance=book)
        return render(request, 'livrowebapp/editbooks.html', {'member': member_data, 'form': form, 'book': book})
    else:
        return redirect('profile_writer')
def delete_book(request, book_id):
    member_data = request.session.get('member', None)
    if member_data['type_user'] == 'Writer':
        book = get_object_or_404(Book, id=book_id, uploader_user=member_data['username'])
        if request.method == 'POST':
            book.delete()
            messages.success(request, 'Book deleted successfully!')
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    else:
        return JsonResponse({'success': False, 'error': 'Permission denied'})
def custom_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is signed in using your custom session logic
        member_data = request.session.get('member', None)
        if not member_data:
            # If not signed in, redirect to your signin page or any other page
            return redirect('signin')

        # If signed in, proceed with the original view function
        return view_func(request, *args, **kwargs)

    return _wrapped_view
@custom_login_required

def bookinformation(request, title):
    member_data = request.session.get('member', None)
    book = get_object_or_404(Book, title=title)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        liked = request.POST.get('liked', None)

        if liked:
            user = Member.objects.get(username=member_data['username'])
            user_fave, created = UserFave.objects.get_or_create(user=user, book=book)
            user_fave.liked = not user_fave.liked
            user_fave.save()

        elif comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = Member.objects.get(username=member_data['username'])
            new_comment.book = book
            new_comment.save()

        return redirect('bookinformation', title=title)

    else:
        comment_form = CommentForm()

    comments = book.comments.all()
    print(comments)
    likes_count = book.userfave_set.filter(liked=True).count()

    liked_status = None
    if member_data:
        user = Member.objects.get(username=member_data['username'])
        user_fave = UserFave.objects.filter(user=user, book=book).first()
        if user_fave:
            liked_status = user_fave.liked

    context = {
        'book': book,
        'comments': comments,
        'comment_form': comment_form,
        'likes_count': likes_count,
        'user': member_data,
        'liked_status': liked_status,
    }

    return render(request, 'livrowebapp/bookinformation.html', context)
def home(request):
    return render(request, 'livrowebapp/home.html')

def browse(request):
    member_data = request.session.get('member', None)

    # Check for the login_required query parameter
    login_required_param = request.GET.get('login_required', None)
    if login_required_param:
        messages.warning(request, 'You need to sign in first.')

    all_books = Book.objects.all()
    for book in all_books:
        book.genre_list = book.genre.split(', ')

    # Include the messages in the template context
    messages_data = messages.get_messages(request)

    return render(request, 'livrowebapp/browse.html', {'member': member_data, 'all_books': all_books, 'messages_data': messages_data})
def fantasy(request):
    return render(request, 'livrowebapp/books/fantasy.html')
def action(request):
    return render(request, 'livrowebapp/books/action.html')
def browse_content(request):
    member_data = request.session.get('member', None)
    all_books = Book.objects.all()
    return render(request, 'livrowebapp/browse-content.html', {'member': member_data, 'all_books': all_books})
def logout(request):
    if 'member' in request.session:
        del request.session['member']
    return redirect('browse')