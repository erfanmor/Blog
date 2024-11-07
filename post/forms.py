from django import forms
from .models import Post, Comments, CommentsReplay, Tag


class AddNewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags', 'photo']

    def __init__(self, *args, **kwargs):
        super(AddNewPostForm, self).__init__(*args, **kwargs)

        # Use CheckboxSelectMultiple
        self.fields['tags'].widget = forms.CheckboxSelectMultiple()
        self.fields['tags'].queryset = Tag.objects.all()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['body']
        labels = {
            'body': 'Comments'
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

        self.fields['body'].widget.attrs.update({'class': 'form-control'})
        self.fields['body'].widget.attrs.update({'rows': '3'})
        self.fields['body'].widget.attrs.update(
            {'placeholder': 'Write your comment'})
        self.fields['body'].widget.attrs.update(
            {'label': 'Write your comment'})


class CommentReplayForm(forms.ModelForm):
    class Meta:
        model = CommentsReplay
        fields = ['body', 'replay_to']
