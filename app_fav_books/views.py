from django.shortcuts import render, redirect
from .models import User, Book
from django.contrib import messages
import bcrypt
from bcrypt import checkpw

def index(request):
  return render(request, 'index.html')


def register(request):
  print('\n------------ REGISTER METHOD ---------')
  if request.method == "POST":
    print(request.POST)
    errors = User.objects.validate_user_registration(request.POST)
    if errors:
      for key, value in errors.items():
        messages.error(request, value, extra_tags="danger")
      return redirect('/')
    else:
      print('\n-------------- register success no errors!')
      # create User
      first_name = request.POST['first_name']
      last_name = request.POST['last_name']
      email = request.POST['email']
      # birthday = request.POST['birthday']
      password = request.POST['password']
      hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
      created_user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hashed_pw) 
      request.session['user_id'] = created_user.id
      request.session['user_first_name'] = created_user.first_name
      messages.success(request, "Welcome from Registration")
      return redirect('/books')
  return redirect('/')



def login(request):
  print('\n------------ LOGIN METHOD ---------')
  if request.method == "POST":
    print(request.POST)
    errors = User.objects.validate_user_login(request.POST)
    if errors:
      for key, value in errors.items():
        messages.error(request, value, extra_tags="danger")
      return redirect('/')
    else :
      user = User.objects.get(email=request.POST['email'])
      request.session['user_id'] = User.objects.get(email=request.POST['email']).id
      request.session['user_first_name'] = User.objects.get(email=request.POST['email']).first_name
      messages.success(request, f'Welcome {user.first_name} from login', extra_tags="success")
      return redirect('/books')
  return redirect('/')


def logout(request):
  print('\n --------- LOGOUT ⛔ -------')
  if 'user_id' in request.session:
    # request.session.pop('user_id')
    request.session.clear()
    messages.warning(request, "session cleared - user logged out!")
    return redirect('/')
  else:
    messages.warning(request, "nothing to clear", extra_tags="warning")
    return redirect('/')
  
  
  
  
  
# ======================= BOOKS ====================

def books_page(request):
  print('\n------------ THE BOOKS PAGE ---------')
  if 'user_id' not in request.session:
    messages.error(request, "please log in", extra_tags="warning")
    return redirect('/')
  this_user = User.objects.get(id=request.session['user_id'])
  # get all books
  context = {
    'all_books' : Book.objects.all(),
    'this_user_fav_books' : this_user.liked_books.all()
  }
  return render(request, 'books_page.html', context)


def create(request):
  print('--- create method  ---')
  if request.method == 'POST':
    print(request.POST)
    errors = Book.objects.book_validation(request.POST)
    if errors:
      for key, val in errors.items():
        messages.error(request, val, extra_tags="danger")
      return redirect('/books')
    else:
      # no book errros go and pass it in db with user logged in
      title = request.POST['title']
      description = request.POST['description']
      # books uploaded should auto favorite
      current_user = User.objects.get(id=request.session['user_id'])
      created_book = Book.objects.create(title=title, description=description, uploaded_by=current_user)
      created_book.users_who_like.add(current_user)
      messages.success(request, "Successfully CREATED a  book!", extra_tags="success")
  return redirect('/books')
  



def check_if_edit_or_show(request, book_id):
  print('\n------------ edit? or view? method check ---------')
  print('book_id->', book_id)
  this_book_user_id = Book.objects.get(id=book_id).uploaded_by.id
  this_user_id = request.session['user_id']
  if this_book_user_id == this_user_id:
    print('\n\nthis_book_user_id ->', this_book_user_id)
    print('this_user_id ->', this_user_id)
    print('going to edit page!')
    return redirect(f'/edit_book_page/{book_id}')
  else:
    return redirect(f'/show_book_page/{book_id}')
  
def edit_book_page(request, book_id):
  print('--- edit_book_page html ---')
  print('book_id->',book_id)
  # prepopulate book fields'
  context = {
    'this_book' : Book.objects.get(id=book_id)
  }
  return render(request, 'edit_book_page.html', context)

def show_book_page(request, book_id):
  print('------------- show_book_page html -------------')
  print('book_id->',book_id)
  #get that book
  context = {
    # 'this_books_users_who_like' : Book.objects.get(id=book_id).users_who_like.all(),
    # 'this_user' : User.objects.get(id=request.session['user_id']),
    'this_book' : Book.objects.get(id=book_id),
    'all_users_who_like' : Book.objects.get(id=book_id).users_who_like.all() 
  }
  return render(request, 'show_book_page.html', context)

def update(request):
  print('------------ update method -------------')
  print(request.POST)
  book_id = request.POST['book_id']
  print('\nbook_id->', book_id)
  # check book for edit
  errors = Book.objects.book_validation(request.POST)
  if errors:
    for key, val in errors.items():
      messages.error(request, val, extra_tags="danger")
    return redirect(f'/edit_book_page/{book_id}')
  else:
    # no book errros go and UPDATE in db with user logged in
    title = request.POST['title']
    description = request.POST['description']
    # books uploaded should auto favorite
    # current_user = User.objects.get(id=request.session['user_id'])
    book_to_update = Book.objects.get(id=book_id)
    book_to_update.title = title
    book_to_update.description = description
    book_to_update.save()
    messages.success(request, "Successfully updated book!", extra_tags="success")
    # created_book.users_who_like.add(current_user)
  return redirect(f'/show_book_page/{book_id}')


def like_this_book(request, book_id):
  print('------------ like_this_book method ❤-------------')
  this_user = User.objects.get(id=request.session['user_id'])
  # like this book
  Book.objects.get(id=book_id).users_who_like.add(this_user)
  messages.success(request, "You ❤ a book!", extra_tags="success")
  return redirect('/books')

def unlike(request, book_id):
  print('------------- unlike method ❌-----------------')
  this_user = User.objects.get(id=request.session['user_id'])
  # unlike this book
  Book.objects.get(id=book_id).users_who_like.remove(this_user)
  messages.success(request, "You unliked a book! ❌", extra_tags="success")
  return redirect('/books')



def delete(request):
  print('-------------- delete method ❌--------------')
  book_id = request.POST['book_id']
  Book.objects.get(id=book_id).delete()
  messages.success(request, "Successfully DELETED book!", extra_tags="warning")
  print('\nbook_id->', book_id)
  return redirect('/books')