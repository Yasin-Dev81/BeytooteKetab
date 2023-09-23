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
        return cd


class EmailForm(forms.Form):
    email = forms.EmailField(
        label="ایمیل",
        widget=forms.EmailInput(attrs={"class": "form__input", "type": "text", "placeholder": "ایمیل"})
    )

    def save(self, user, commit=True):
        cd = self.cleaned_data
        user.email = cd["email"]
        if commit:
            user.save()
        return cd
