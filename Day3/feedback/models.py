from django.db import models

# Create your models here.
class Feedback(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    

# student management system basic
class Student(models.Model):
    GENDER_CHOICES=[
        ('M','MALE'),
        ('F','FEMALE'),
    ]
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    age=models.IntegerField()
    department=models.CharField(max_length=20)
    gender=models.CharField(
        max_length=1,
        choices=GENDER_CHOICES
    )
    cgpa=models.FloatField(default=0.0)
    isactive=models.BooleanField(default=True)
    admission_date=models.DateField()
    
    def __str__(self):
        return self.name
    
# for blog system
class Category(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Post(models.Model):
    title=models.CharField(max_length=20)
    slug=models.SlugField(unique=True)
    content=models.TextField(max_length=300)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_published=models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
# for ecommerce system
class Product(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.DecimalField()
    stock=models.IntegerField(
        validators=[MinValueValidator(0)]
    )
    image=models.ImageField(upload_to='products/')
    product_url=models.URLField(blank=True)
    is_available=models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

# for user profile system 
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    bio=models.TextField(max_length=100)
    profile_picture=models.ImageField(upload_to='profile_picture/',blank=True,null=True)
    website=models.URLField(blank=True)
    phone=models.CharField(max_length=20,blank=True)
    def __str__(self):
        return self.user.username

# for course enrollment system 
class Course(models.Model):
    title=models.CharField(max_length=20)
    duration=models.IntegerField()
    def __str__(self):
        return self.title
    
class CourseStudent(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField()
    course=models.ManyToManyField(Course)
    def __str__(self):
        return self.name


# for job portal model 

class Company(models.Model):
    name=models.CharField(max_length=10)
    website=models.URLField()
    def __str__(self):
        return self.name

class Job(models.Model):
    JOB_TYPE=[
        ('R','Remote'),
        ('O','Offline'),
        ('H','Hybrid'),
    ]
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    description=models.TextField()
    salary=models.IntegerField()
    location=models.CharField(max_length=100)
    job_type=models.CharField(max_length=10,choices=JOB_TYPE,default='O')
    deadline=models.DateTimeField()
    posted_at=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(True)
    
    def __str__(self):
        return self.title