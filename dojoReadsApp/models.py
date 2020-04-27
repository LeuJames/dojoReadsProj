from django.db import models
import re, bcrypt

class userManager(models.Manager):

    def register_validator(self,postData):
        errors = {}
        if len(postData['name']) < 2:
            errors['name'] = "Name name must be filled out and at least 2 characters long!"
        if len(postData['alias']) < 2:
            errors['alias'] = "Alias must be filled out and at least 2 characters long!"

        # Checks email format (make sure to import re)
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):         
            errors['email'] = "Invalid email address!"

        # looks to see if email is already in database
        elif len(User.objects.filter(email=postData['email'])) > 0:
            errors['existingEmail'] = "Email is already taken by another user"
        
        # Checks length of password, and if long enough, will check the passwords against eachother
        if len(postData['pw']) < 8:
            errors['pw'] = "Password must be at least 8 characters!"
        elif postData['pw'] != postData['confirm_pw']:
            errors['confirm_pw'] = "Password does not match confirm password field!"

        return errors

    def login_validator(self,postData):
        errors = {}
        # Checks to see if email matches record in db
        user = User.objects.filter(email=postData['email'])
        if len(user) < 1:
            errors['emailDoesNotExist'] = "Email does not exist"

        # if email exists, checks inputted password (bcypt hashed) against the record's hashed pw
        else:
            logged_user = user[0]
            if not bcrypt.checkpw(postData['pw'].encode(), logged_user.password.encode()):
                errors['badPW'] = "Password is incorrect!!"
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = userManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    review = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey(User, related_name="reviews", on_delete = models.CASCADE)
    book = models.ForeignKey(Book, related_name="reviews", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)