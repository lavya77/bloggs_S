from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Profile

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # We only include the fields that exist in your Post model
        fields = ['title', 'description']
        
        # Define common styling for text-based inputs
        text_input_class = 'w-full px-4 py-3 bg-gray-50 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition duration-200 ease-in-out'
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': text_input_class,
                'placeholder': 'Enter the post title',
            }),
            'description': forms.Textarea(attrs={
                'class': text_input_class,
                'rows': 10,
                'placeholder': 'Write your full post content here...',
            }),
        }



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # This should be the name of the text field in your Comment model
        fields = ['content'] 
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 1, # Make it a single line initially
                'placeholder': 'Add a comment...', # This text will appear in the box
                'class': 'your-tailwind-css-classes' # This will be styled by the <style> block in the template
            })
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        # Include the fields from your model that you want to be editable
        fields = ['bio', 'profile_pic']
        
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500',
                'rows': 4,
                'placeholder': 'Tell us a little about yourself...'
            }),
            'profile_pic': forms.FileInput(attrs={
                'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'
            })
        }
