from __future__ import unicode_literals

from django.db import models

import re

# Defining regular expressions for each of the fields
FN_REGEX = re.compile(r'^[a-zA-Z]{2,}$')  # first name
LN_REGEX = re.compile(r'^([a-zA-Z]){2,}$')  # last name
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')  # email
PWD_REGEX = re.compile(r'^.{8,}$') # password

# Create your models here.
class RegisterManager(models.Manager):
    def validateFN(self, first_name):
        fnChk = False
        msg = ""

        if (len(first_name) < 1):
            msg = "First name cannot be blank!"
        elif not FN_REGEX.match(first_name):
            msg = "Invalid first name!"
        else:
            fnChk = True
        
        return (fnChk, msg)

    def validateLN(self, last_name):
        lnChk = False
        msg = ""

        if (len(last_name) < 1):
            msg = "Last name cannot be blank!"
        elif not LN_REGEX.match(last_name):
            msg = "Invalid last name!"
        else:     
            lnChk = True
        
        return (lnChk, msg)

    def validateEmail(self, email):
        emailChk = False
        msg = ""

        if len(email) < 1:
            msg = "Email cannot be blank!"
        elif not EMAIL_REGEX.match(email):
            msg = "Invalid Email Address!"
        else: 
            emailChk = True

        return (emailChk, msg)

    def validatePwd(self, pwd):
        pwdChk = False
        msg = ""
        
        if len(pwd) < 1:
            msg = "Password cannot be blank!"
        elif not PWD_REGEX.match(pwd):
            msg = "Invalid password cannot be blank!"
        else: 
            pwdChk = True
        
        return (pwdChk, msg)
    
    def chkRegister(self, email):
        registerChk = False

        email_list = Register.objects.filter(email=email)
        if (len(email_list) != 0):  # Making sure email list is not empty
            for userEmail in email_list:
                if userEmail.email == email:
                    registerChk = True
                    break

        return (registerChk)

class Register(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    pwd_confirm = models.CharField(max_length=255)

    objects = models.Manager()  # Default manager
    registerManager = RegisterManager()  # Register specific manager