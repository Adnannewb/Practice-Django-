from django import forms
from .models import Feedback    

class FeedbackForm(forms.ModelForm):
    class Meta:
        model=Feedback
        fields=['name','email','message']
        widgets={
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter your name'
            }),

            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email'
            }),

            'message': forms.Textarea(attrs={
                'placeholder': 'Write your message',
                'rows': 5
            }),
        }

# student management system basic

class StudentForm(forms.ModelForm):
    class Meta:
        model=Student
        fields='__all__'
        labels={
            'cgpa':'Current CGPA',
        }
        widgets={
            'name':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter Name'
                
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Email'
            }),

            'age': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'department': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'gender': forms.Select(attrs={
                'class': 'form-select'
            }),

            'cgpa': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'admission_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            })
            
        }
        

# for blog system

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        exclude=['created_at','updated_at']
        widgets={
            'tittle':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter Title'
            }),
            'slug':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter Slug'
            }),
            'content':forms.Textarea(attrs={
                'class':'form-control',
                'rows':5,
            }),
            'category':forms.Select(attrs={
                'class':'form-select',
            }),
        }

# for ecommerce system
class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields='__all__'
        widgets={
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control'
            }),

            'price': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'stock': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),

            'product_url': forms.URLInput(attrs={
                'class': 'form-control'
            })
        }

# for user profile system
class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=['user']
        widgets={
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),

            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control'
            }),

            'website': forms.URLInput(attrs={
                'class': 'form-control'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control'
            })
        }

# for course enrollment system 

class CourseEnrollmentForm(forms.ModelForm):

    class Meta:
        model = CourseStudent
        fields = ['name', 'email', 'courses']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),

            'courses': forms.CheckboxSelectMultiple()
        }
        
        
# for job portal model 
class JobForm(forms.ModelForm):
    class Meta:
        model=Job
        exclude=['posted_at']
        
        widgets = {
        'company': forms.Select(attrs={
            'class': 'form-select'
        }),

        'title': forms.TextInput(attrs={
            'class': 'form-control'
        }),

        'description': forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5
        }),

        'salary': forms.NumberInput(attrs={
            'class': 'form-control'
        }),

        'location': forms.TextInput(attrs={
            'class': 'form-control'
        }),

        'job_type': forms.Select(attrs={
            'class': 'form-select'
        }),

        'deadline': forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
    }
    
