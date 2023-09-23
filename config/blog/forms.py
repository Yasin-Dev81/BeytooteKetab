from django import forms

from .models import BlogComment


class BlogCommentForm(forms.Form):
    text = forms.CharField(
        label="کامنت",
        widget=forms.Textarea(attrs={"class": "form__textarea", "placeholder": "افزودن دیدگاه"})
    )

    def save(self, blog, user, commit=True):
        cd = self.cleaned_data
        comment = BlogComment.objects.create(
            text=cd['text'],
            blog=blog,
            author=user
        )
        if commit:
            comment.save()
        return comment
