from django.db import models
import re, bcrypt 
import datetime

# Create your models here.
class UserVald(models.Manager):
    def uservalidation(self, postData):
        errors = {}
        usernameMatch = User.objects.filter(username= postData['username'])
        if len(postData['name']) < 3:
            errors['name'] = "First name should have more than 3 character"
        if len(postData['username']) < 3:
            errors['username'] = "Username should have more that what you just put in"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 character"
        if postData['password'] != postData['confirmpass']:
            errors['confirmpass'] = "Password does not match"
        if len(usernameMatch)>0:
            errors['userMatch'] = "Username taken"
        return errors
    def loginvalidation(self, postData):
        errors = {}
        usernameCheck = User.objects.filter(username = postData['username'])
        if usernameCheck:
            logged_user = usernameCheck[0]

            if bcrypt.checkpw(postData['password'].encode(), logged_user.password.encode()):
                pass
            else:
                errors['wrongpass'] = "Password does not match"
        else:
            errors['nonuser'] = "Username doesn't exist"
        
        return errors

class Travelvald(models.Manager):
    def tripvalidation(self, postData):
        errors = {}
        if len(postData['dest']) < 5:
            errors['desmessing'] = "You need to add a destination"
        if len(postData['des']) < 5:
            errors['description'] = "Description Missing"
        if len(postData['tdf']) < 1:
            errors["thedatefrom"] = "Date from missing"
        if len(postData['tdt']) < 1:
            errors["thedateto"] = "Date to missing"
        present = datetime.date.today()
        if postData['tdf'] <= str(present):
            errors['date1'] = "Date should be in the future"
        if postData['tdf'] > postData['tdt']:
            errors['date2'] = "ERROR"
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserVald()

class Travel(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField()
    traveldatefrom = models.DateTimeField()
    traveldateto = models.DateTimeField()
    planer = models.ForeignKey(User, related_name="trips", on_delete = models.CASCADE)
    jointrip = models.ManyToManyField(User, related_name = "jointrips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Travelvald()