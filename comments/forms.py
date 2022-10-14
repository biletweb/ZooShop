from django import forms
from comments.models import Comments


class CommentAddForm(forms.ModelForm):
    comment = forms.CharField(label='Комментарий', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10}))

    class Meta:
        model = Comments
        fields = ('comment', )
