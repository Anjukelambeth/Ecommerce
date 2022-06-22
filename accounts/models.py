from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.core.validators import RegexValidator,MinLengthValidator
# Create your models here.
phone_regex = RegexValidator(regex=r'^\+?1?\d{9,13}$', 
                                message = "Phone number must be entered in the format: '+999999999999'. Up to 13 digits allowed.")
nameMinlength=MinLengthValidator(3,'Min 3 char required')
nameValidator=RegexValidator(regex=r'^[A-Za-z][A-Za-z ]*$',message ="Enter a valid name")

# extra_kwargs = {'phone': {'error_messages': {'blank': 'New blank error message'}}}

class MyAccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,user_name,email,phone_number,password=None):
        if not email:
            raise ValueError('Username must be there')
        if not user_name:
            raise ValueError('user  must have a username')
        if not phone_number:
            raise ValueError('Prvode a valid mobile number')

        user  = self.model(
            email=self.normalize_email(email),
            user_name =  user_name,
            first_name = first_name,
            last_name = last_name,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using= self.db)
        return user
    def create_superuser(self,first_name,last_name,email,user_name,phone_number,password = None):
        user = self.create_user(
            email=self.normalize_email(email),
            user_name=user_name,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,

        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using = self._db)
        return user

class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50,validators=[nameValidator,nameMinlength])
    last_name = models.CharField(max_length=50,validators=[nameValidator,nameMinlength])
    user_name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=13,validators=[phone_regex],blank=False, unique=True)
    

    #required 
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff =  models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    #login field
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name','first_name','last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email
    def has_perm(self,perm, obj=None):
        return self.is_admin
    def has_module_perms(self, add_label):
        return True
    # user= models.OneToOneField(User,null=False,blank=False,on_delete=models.CASCADE)

    # #extra fields
    # phone_number = models.CharField(max_length=10,null=False,validators=[phone_regex],blank=False, unique=True)

    # # def __str__(self):
    # #     return self.user.username
class UserAddresses(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE,null=True)
    first_name = models.CharField(max_length=50,blank=True, null=True)
    last_name = models.CharField(max_length=50,blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)   
    address_line_1=models.CharField(max_length=200,blank=True)
    address_line_2=models.CharField(max_length=200,blank=True)
    city=models.CharField(max_length=200,blank=True)
    zipcode=models.CharField(max_length=200,blank=True)
    state=models.CharField(max_length=200,blank=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    

    def __str__(self):
        return self.address_line_1
    
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

    def  full_name(self):
        return f'{self.first_name} {self.last_name}'
        
    