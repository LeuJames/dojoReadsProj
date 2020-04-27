from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

# All methods after login & registration check to see that user is logged in before routing (if 'userID' in request.session)

# Load login & registration page
def index(request):
    return render(request, 'index.html')

# Register function that validates registration form data & creates new user record with brypt hashed password. Creates session with user's name & redirects to the wall page (through /success route)
def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags='register') # extra tag to distinguish registration message from login message
        return redirect('/')
    password = request.POST['pw']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    print(pw_hash)
    newUser = User.objects.create(
        name=request.POST['name'],
        alias=request.POST['alias'],
        email=request.POST['email'],
        password=pw_hash,
        )
    request.session['userID'] = newUser.id
    return redirect('/books')

# Login function that validates login form data & logs creates user session, redirects to wall page through /success route.
def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags='login')
            return redirect('/')
    request.session['userID']=User.objects.get(email=request.POST['email']).id
    return redirect('/books')

# clears session & returns to login page
def logout(request):
    request.session.clear()
    return redirect ('/')

# books route only allows routing to wall page if name is in session
def books(request):
    if 'userID' in request.session:
        context = {
            'name' : User.objects.get(id=request.session['userID']).name,
            'books' : Book.objects.all(),
            'recentReviews' : Review.objects.all().order_by('-id')[:3],
        }
        return render(request, 'books.html', context)
    return redirect ('/')

# books/add runs addBook method which renders addBook html page 
def addBook(request):
    if 'userID' in request.session:
        context = {
            'authors' : Book.objects.values_list('author', flat=True)
        }
        return render(request, 'addBook.html', context)
    return redirect ('/')

# submitBook route takes in form post request to create new book and associated review. 
# If/elif statements check to see whether the dropdown or text field was used to input author. 
# Creates review either way. 
# Need to add validation to make sure that book is created properly before review is created.
def submitBook(request):
    if 'userID' in request.session:
        if 'authorSelect' in request.POST:
            newBook = Book.objects.create(
                title = request.POST['title'],
                author = request.POST['authorSelect']
                )
        elif request.POST['authorInput'] != '':
            newBook = Book.objects.create(
                title = request.POST['title'],
                author = request.POST['authorInput']
                )
        Review.objects.create(
            review= request.POST['review'],
            rating= request.POST['rating'],
            user= User.objects.get(id=request.session['userID']),
            book= Book.objects.get(id=newBook.id)
            )
        return redirect(f'/books/{newBook.id}')
    return redirect ('/')

def bookPage(request,bookID):
    if 'userID' in request.session:
        context = {
            'book' : Book.objects.get(id=bookID),
            'reviews' : Review.objects.filter(book = Book.objects.get(id=bookID)),
        }
        return render(request, 'bookpage.html', context)
    return redirect ('/')

def submitReview(request, bookID):
    if 'userID' in request.session:
        Review.objects.create(
            review= request.POST['review'],
            rating= request.POST['rating'],
            user= User.objects.get(id=request.session['userID']),
            book= Book.objects.get(id=bookID)
            )
        return redirect(f'/books/{bookID}')
    return redirect ('/')

def userPage(request, userID):
    if 'userID' in request.session:
        context = {
            'user' : User.objects.get(id=userID),
            'reviews' : Review.objects.filter(user=User.objects.get(id=userID))
        }
        return render(request, 'userPage.html', context)
    return redirect ('/')

def deleteReview(request, reviewID):
    reviewToDelete = Review.objects.get(id=reviewID)
    print(reviewToDelete.user.id)
    print(request.session['userID'])
    if request.session['userID'] == reviewToDelete.user.id:
        bookID = reviewToDelete.book.id
        reviewToDelete.delete()
        return redirect(f'/books/{bookID}')
    return redirect ('/')
