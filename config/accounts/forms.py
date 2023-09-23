from django import forms
from .models import User, OtpCode
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='password',
        widget=forms.PasswordInput(
            attrs={"class": "sign__input", "placeholder": 'شماره موبایل'}
        )
    )
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'full_name',
            'phone_number',
            'email'
        )

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('passwords dont match')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text="you can change password using <a href=\"../password/\">this form</a>.")

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name', 'password', 'last_login')


class UserRegistrationForm(forms.Form):
    phone = forms.CharField(
        max_length=11,
        label="شماره موبایل",
        help_text="بدون پیش شماره +98 وارد کنید",
        widget=forms.TextInput(attrs={"class": "sign__input", "placeholder": '09000000000'})
    )
    # email = forms.EmailField(
    #     widget=forms.EmailInput(attrs={"class": "sign__input", "placeholder": 'ایمیل'})
    # )
    full_name = forms.CharField(
        label='نام و نام خانوادگی',
        # help_text="نامی مستعار یا دلخواه وارد کنید",
        widget=forms.TextInput(attrs={"class": "sign__input", "placeholder": 'یاسین خوش منش'})
    )
    password1 = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(attrs={"class": "sign__input", "placeholder": 'رمز عبور'})
    )
    password2 = forms.CharField(
        label='تکرار رمز عبور',
        # help_text="رمز باید به حاوی حروف بزرگ و کوچک انگلیسی و اعداد باشد",
        widget=forms.PasswordInput(attrs={"class": "sign__input", "placeholder": 'تکرار رمز عبور'})
    )

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if not email:
    #         print("------------------- email is blank")
    #     user = User.objects.filter(email=email).exists()
    #     if user:
    #         raise ValidationError('This email already exists')
    #     return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        user = User.objects.filter(phone_number=phone).exists()
        if user:
            raise ValidationError('اکانتی با این شماره وجود دارد!')
        OtpCode.objects.filter(phone_number=phone).delete()
        return phone

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('پسوردها یکی نیستند!')
        if len(cd['password1']) < 8:
            raise ValidationError("پسورد باید دارای حداقل طول 8 باشد!")
        if not any(x.isupper() for x in cd['password1']):
            raise ValidationError("پسورد باید حاوی حداقل یک حرف بزرگ انگلیسی باشد!")
        if not any(x.isdigit() for x in cd['password1']):
            raise ValidationError("پسورد باید حاوی حداقل یک عدد باشد!")

        return cd['password2']


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField(
        label="کد ارسالی را وارد کنید",
        widget=forms.TextInput(attrs={"class": "sign__input", "placeholder": 'XXXX'})
    )

    def clean_code(self):
        cd = self.cleaned_data
        if not len(str(cd['code'])) == 4:
            raise ValueError('طول کد درست نیست!')
        return cd['code']


class UserLoginForm(forms.Form):
    phone = forms.CharField(
        max_length=11,
        label="شماره موبایل",
        help_text="بدون پیش شماره +98 وارد کنید",
        widget=forms.TextInput(attrs={"class": "sign__input", "placeholder": '09000000000'})
    )
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(attrs={"class": "sign__input", "placeholder": 'رمز عبور'})
    )


class UserPasswordResetForm(forms.Form):
    phone = forms.CharField(
        max_length=11,
        label="شماره موبایل",
        help_text="بدون پیش شماره +98 وارد کنید",
        widget=forms.TextInput(attrs={"class": "sign__input", "placeholder": '09000000000'})
    )

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        user = User.objects.filter(phone_number=phone).exists()
        if not user:
            raise ValidationError('اکانتی با این شماره وجود ندارد!')
        OtpCode.objects.filter(phone_number=phone).delete()
        return phone


class UserPasswordResetVerifyCodeForm(forms.Form):
    code = forms.IntegerField(
        label="کد ارسالی را وارد کنید",
        widget=forms.TextInput(attrs={"class": "sign__input", "placeholder": 'XXXX'})
    )
    password1 = forms.CharField(
        label="رمز عبور جدید",
        widget=forms.PasswordInput(attrs={"class": "sign__input", "placeholder": 'رمز عبور'})
    )
    password2 = forms.CharField(
        label='تکرار رمز عبور جدید',
        # help_text="رمز باید به حاوی حروف بزرگ و کوچک انگلیسی و اعداد باشد",
        widget=forms.PasswordInput(attrs={"class": "sign__input", "placeholder": 'تکرار رمز عبور'})
    )

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('پسوردها یکی نیستند!')
        if len(cd['password1']) < 8:
            raise ValidationError("پسورد باید دارای حداقل طول 8 باشد!")
        if not any(x.isupper() for x in cd['password1']):
            raise ValidationError("پسورد باید حاوی حداقل یک حرف بزرگ انگلیسی باشد!")
        if not any(x.isdigit() for x in cd['password1']):
            raise ValidationError("پسورد باید حاوی حداقل یک عدد باشد!")

        return cd['password2']


class EditUserInfoForm(forms.Form):
    phone = forms.CharField(
        max_length=11,
        label="شماره موبایل",
        help_text="بدون پیش شماره +98 وارد کنید",
        widget=forms.TextInput(attrs={"class": "sign__input", "placeholder": '09000000000'})
    )
    email = forms.EmailField(
        label="ایمیل",
        widget=forms.EmailInput(attrs={"class": "sign__input", "placeholder": 'ایمیل'})
    )
    full_name = forms.CharField(
        label='نام و نام خانوادگی',
        # help_text="نامی مستعار یا دلخواه وارد کنید",
        widget=forms.TextInput(attrs={"class": "sign__input", "placeholder": 'یاسین خوش منش'})
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        # print('--'*10, self.request)
        super(EditUserInfoForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        if self.request.user.email == email:
            return email

        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('این ایمیل قبلا ثبت شده است!')
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if self.request.user.phone_number == phone:
            return phone

        user = User.objects.filter(phone_number=phone).exists()
        if user:
            raise ValidationError('اکانتی با این شماره وجود دارد!')
        OtpCode.objects.filter(phone_number=phone).delete()
        return phone

    def save(self, commit=True):
        cd = self.cleaned_data
        self.request.user.phone_number = cd['phone']
        self.request.user.email = cd['email']
        self.request.user.full_name = cd['full_name']
        if commit:
            self.request.user.save()
        return self.request.user
