from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
import bcrypt
import re

class UserManager(models.Manager):
    def nameValidator(self, postData):
        errors = {}
        if len(postData['fullname']) < 2:
            errors['lengthtName'] = "First name must be at least 2 characters."
        elif not re.match('[A-Za-z]+', postData['fullname']):
            errors['nameValid'] = "First name must only contain letters."

        if len(postData['email']) < 1:
            errors['lengthEmail'] = "Email is required."
        elif not re.match('[A-Za-z-0-9-_]+(.[A-Za-z-0-9-_]+)*@[A-Za-z-0-9-_]+(.[A-Za-z-0-9-_]+)*(.[A-Za-z]{2,})', postData['email']):
            errors['emailValid'] = "Email not valid."
        elif User.objects.filter(email=postData['email']):
            errors['emailTaken'] = "Email was already registered."

        if len(postData['alias']) < 1:
            errors['lengthalias'] = "username is required."
        elif User.objects.filter(alias=postData['alias']):
            errors['aliasnameTaken'] = "alias was already registered."

        if len(postData['password']) < 8:
            errors['lengthPassword'] = "Password must be at least 8 characters."
        if postData['password'] != postData['confirm_password']:
            errors['passConfirmPassword'] = "Passwords do not match."
        return errors

    def loginValidator(self, postData):
        errors = {}
        if len(postData['email']) < 1:
            errors['noEmail'] = "Please input an email."
        elif not re.match('[A-Za-z-0-9-_]+(.[A-Za-z-0-9-_]+)*@[A-Za-z-0-9-_]+(.[A-Za-z-0-9-_]+)*(.[A-Za-z]{2,})', postData['email']):
            errors['emaiValid'] = "Email is not valid."
        elif not User.objects.filter(email=postData['email']):
            errors['emailExist'] = "This email is not registered in our database."

        if len(postData['password']) < 1:
            errors['noPass'] = "Please input a password."
        elif bcrypt.checkpw(postData['password'].encode(), User.objects.get(email=postData['email']).password.encode()) == False:
            errors['incorrect_pass'] = "Incorrect password: does not match password stored in database."
        return errors

class QuoteManager(models.Manager):
    def QuoteManager(self, postData):
        errors = {}
        if len(postData['quotedby']) < 3:
            errors['itemLength'] = "name longer than 3 characters"
        if len(postData['message']) < 10:
            errors['itemLength'] = "quote must be longer than 10 characters"
            return errors

class User(models.Model):
    fullname = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Quote(models.Model):
    quotedby = models.CharField(max_length = 255)
    message = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    added_by = models.ForeignKey(User, related_name = 'create')
    liked_users = models.ManyToManyField(User, related_name = 'liked_quotes')
    objects = QuoteManager()