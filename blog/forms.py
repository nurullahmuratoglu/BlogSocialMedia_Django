from django import forms
from .models import Blog,Comment
from ckeditor.widgets import CKEditorWidget


class BlogForm(forms.ModelForm):
    icerik=forms.CharField(widget=CKEditorWidget())
    class Meta:
        model=Blog
        fields={'title','resim','kategori','icerik'}
    def __init__(self,*args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
            self.fields['icerik'].widget.attrs['rows'] = 20



class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['icerik']
        widgets = {
            'icerik': forms.Textarea(attrs={'rows': 3, 'cols': 55}),
        }

        def __init__(self, *args, **kwargs):
            super(CommentForm, self).__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs = {'class': 'form-control'}

