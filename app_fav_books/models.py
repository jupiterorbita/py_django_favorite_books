from django.contrib.messages.api import error
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from datetime import date, datetime
import re
from bcrypt import checkpw

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9+_-]+@[a-zA-Z0-9_-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
  
  # ============= REGISTER VALIDATIONS ===========
  def validate_user_registration(self, postData):
    today = date.today()
    errors= {}
    first_name = postData['first_name']
    last_name = postData['last_name']
    email = postData['email']
    password = postData['password']
    pw_confirm = postData['pw_confirm']
    # ------ FIRST NAME --------
    if not first_name or first_name.isspace():
      errors['first_name'] = "Please enter a FIRST name!"
    elif len(first_name) < 2:
      errors['first_name'] = "FIRST Name should be at least 2 letters!"
    # elif not first_name.isalpha():
    #   errors['first_name'] = 'FIRST name cannot be special characters!'
    # ------ LAST NAME ---------
    if not last_name or last_name.isspace():
      errors['last_name'] = "Please enter a LAST name!"
    elif len(last_name) < 2:
      errors['last_name'] = "LAST Name should be at least 2 letters!"
    # elif not last_name.isalpha():
    #   errors['last_name'] = 'LAST name cannot be special characters!'
    # ------- EMAIL ----------
    if len(email) < 1:
      errors['email'] = "Email cannot be empty!"
    elif not EMAIL_REGEX.match(email):
      errors['email'] = "Invalid email address!"
    if User.objects.filter(email=email):
      errors['email'] = "EMAIL ALREADY exists! choose another!"
    # ---------- check BIRTHDAY ---------
    # if postData['birthday'] > str(today):
    #   errors['birthday'] = "BIRTHDAY should be in the past!"
    # # check bday AGE
    # birthday = postData['birthday']
    # bday_result = check_birthday(birthday)
    # if bday_result != True:
    #   errors['birthday'] = "you must be over 13 years to register"
    # ---------- PASSWORD ---------
    if not password or password.isspace():
      errors['password'] = "Please enter a PASSWORD!"
    elif len(password) < 8:
      errors['password'] = "PASSWORD must be at least 8 characters!"
    elif password != pw_confirm:
      errors['password'] = "PASSWORD DOES NOT MATCH!"
    return errors
  
  #  ============== LOGIN VALIDATIONS =============
  def validate_user_login(self, postData):
    errors = {}
    email = postData['email']
    password = postData['password']
    # ------- EMAIL CHECK ---------
    if len(email) < 1:
      errors['email'] = "Email cannot be empty!"
    elif not EMAIL_REGEX.match(email):
      errors['email'] = "Invalid email address!"
    # -------- check if email is in DB ------
    elif len(User.objects.filter(email=email)) < 1:
      errors['email'] = "LOGIN ERROR - EMAIL NOT FOUND!"
    else: # if email exists continue to password check
      # retrive the user using email
      user_check = User.objects.filter(email=email)
      if len(password) < 1:
        errors['password'] = "PASSWORD cannot be empty!"
      elif not checkpw(password.encode(), user_check[0].password.encode()):
        errors['password'] = "LOGIN ERROR - PASSWORD not corrent for user"
    return errors
      
# def check_birthday(birthday):  
#   today = str(date.today())
#   today_year_str = ""
#   bday_year_str = ""
  
#   for i in range(len(birthday)-6):
#     bday_year_str += birthday[i]
#   for i in range(len(today)-6):
#     today_year_str += today[i]

#   if (int(today_year_str) - int(bday_year_str)) > 13:
#     return True

class BookManager(models.Manager):
  def book_validation(self, postData):
    
    errors = {}
    title = postData['title']
    description = postData['description']
    
    if len(title) < 1:
      errors['title'] = "Title is required!"
    if len(description) < 1:
      errors['description'] = "Description is required!"
    elif len(description) < 10:
      errors['description'] = "Description must be over 10 characters"
    return errors



class User(models.Model):
  first_name = models.CharField(max_length=80)
  last_name = models.CharField(max_length=80)
  email = models.CharField(max_length=80)
  password = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True) 
  objects = UserManager()
  # liked_books = a list of books user likes
  # books_uploaded = a list of books uploaded by use
  
class Book(models.Model):
  title = models.CharField(max_length=80)
  description = models.TextField()
  uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete=CASCADE)
  users_who_like = models.ManyToManyField(User, related_name="liked_books")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True) 
  objects = BookManager()