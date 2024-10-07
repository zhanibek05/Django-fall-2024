from django import forms 
from datetime import datetime
from django.contrib.auth.models import User
from .models import Comment, Post

class AddPostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields = ['title', 'content']
    # title = forms.CharField(max_length=255, label="Title")
    # content = forms.CharField(widget=forms.Textarea, label="Content")
    # created_at = forms.DateTimeField(initial=datetime.now, label="Date")

class AddCommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Content")
    
    