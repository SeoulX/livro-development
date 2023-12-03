from django import forms
from .models import Member, Book, Library, Feedback

class Memberform(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['username', 'email', 'password', 'type_user', 'about_user']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'access_link', 'description', 'book_cover']
        widgets = {
            'uploader': forms.HiddenInput(),
            'uploader_user': forms.HiddenInput()
        }
        
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['user', 'book', 'likes', 'dislikes', 'comments']
        
