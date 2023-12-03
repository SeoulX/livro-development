from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Q

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
        passw = request.POST.get('passw')
        confirmpass = request.POST.get('confirmpass')
        if(passw == confirmpass):
            form = Memberform(request.POST or None)
            if form.is_valid():
                member = form.save()
                member_active = Member.objects.get(username=usrname, password=passw)
                request.session['member'] = {
                    'username': member_active.username,
                    'email':member_active.email,
                    'password' : member_active.password,
                    'type_user': member_active.type_user,
                    'about_user': member_active.about_user
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
        return render(request, 'livrowebapp/signup.html')
def aboutus(request):
    return render(request, 'livrowebapp/aboutus.html')
def aboutus_logged(request):
    member_data = request.session.get('member', None)
    return render(request, 'livrowebapp/aboutus_logged.html', {'member': member_data})
def browse_reader(request):
    member_data = request.session.get('member', None)
    return render(request, 'livrowebapp/browse_reader.html', {'member': member_data})
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
            return redirect('updatebooks')
        return render(request, 'livrowebapp/deletebook.html', {'member': member_data, 'book': book})
    else:
        # Redirect or handle the case when a non-writer tries to delete a book
        return redirect('profile_writer')
def bookinformation(request, title):
    member_data = request.session.get('member', None)
    book = get_object_or_404(Book, title=title)
    context = {
        'book': book,
    }

    # Render the book information template with the context
    return render(request, 'livrowebapp/bookinformation.html', context)  
def home(request):
    return render(request, 'livrowebapp/home.html')
def browse(request):
    return render(request, 'livrowebapp/browse.html')
def fantasy(request):
    return render(request, 'livrowebapp/books/fantasy.html')
def action(request):
    return render(request, 'livrowebapp/books/action.html')
def browse_content(request):
    member_data = request.session.get('member', None)
    all_books = Book.objects.all()
    return render(request, 'livrowebapp/browse-content.html', {'member': member_data, 'all_books': all_books})