from django.utils import timezone
from django.db import models

class Member(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=16)
    type_user = models.CharField(max_length=10)
    about_user = models.TextField(default='')
    libraries = models.ManyToManyField('Library', related_name='members')
    active = models.BooleanField(default=True) 
    
    def __str__(self):
        return self.username
    
class Library(models.Model):
    library_name = models.CharField(max_length=200)
    book_count = models.IntegerField()
    # Assuming a Library can have multiple books and each book belongs to only one library
    # Renaming the ForeignKey and ManyToManyField relationships
    main_book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='main_libraries')
    books = models.ManyToManyField('Book', related_name='libraries')
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    access_link = models.URLField(null=True, blank=True)
    description = models.TextField()
    book_cover = models.ImageField(upload_to='book_covers/')
    uploader = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='uploaded_books', null=True)
    uploader_user = models.CharField(max_length=200)
    feedbacks = models.ManyToManyField('Feedback', related_name='books')
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    date = models.DateTimeField(auto_now=True) 
    text = models.TextField()

class Rating(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings')
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

class Feedback(models.Model):
    rating = models.OneToOneField(Rating, on_delete=models.CASCADE, related_name='feedback', null=True)
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE, related_name='feedback', null=True)