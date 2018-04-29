from django.db import models
import bcrypt

# Create your models here.
class VALIDATORS(models.Manager):
    def registration_valid(self, postData):
        errors = {}
        if len(postData['password']) < 8:
            errors['password'] = "User's password should be greater than 8 characters"
        if postData['password'] != postData['passwordC']:
            errors['passwordMatch'] ="Passwords do not match"
        if USER.objects.filter(email = postData['email']).exists():
            errors['email'] = "User's email should be unique"
        return errors

    def log_valid(self, postData):
        errors={}
        if USER.objects.filter(email = postData['emailLog']).exists():
            pass
        else:
            errors['UN']='Email does not exist'
            return errors
        if USER.objects.get(email = postData['emailLog']).password != postData['passwordLog']:
            errors['pw'] = 'Password incorrect'
        return errors

    def quote_valid(self, postData):
        errors={}
        if len(postData['author']) < 3:
            errors['name'] = "Author name is too short"
        if len(postData['desc']) < 10:
            errors['quote'] = "Quote is too short"
        return errors


class USER(models.Model):
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    DOB = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    Updated_at = models.DateTimeField(auto_now = True)
    objects = VALIDATORS()

class QUOTES(models.Model):
    author = models.CharField(max_length=255)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    Updated_at = models.DateTimeField(auto_now = True)
    posted_by = models.ForeignKey(USER, on_delete = models.PROTECT)
    fave_by = models.ManyToManyField(USER, related_name = 'fave')
    objects = VALIDATORS()
