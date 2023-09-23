from django import forms

from .models import BookComment


class BookCommentForm(forms.Form):
    text = forms.CharField(
        label="کامنت",
        widget=forms.Textarea(attrs={"class": "form__textarea", "placeholder": "افزودن دیدگاه"})
    )

    def save(self, book, user, commit=True):
        cd = self.cleaned_data
        comment = BookComment.objects.create(
            text=cd['text'],
            book=book,
            author=user
        )
        if commit:
            comment.save()
        return comment
