from django import forms


class CouponApplyForm(forms.Form):
    code = forms.CharField(
        label="کد تخفیف",
        widget=forms.TextInput(attrs={"class": "sign__input", "placeholder": 'XXXX'})
    )

    def clean_code(self):
        cd = self.cleaned_data
        if cd['code']:
            try:
                coupon = Coupon.objects.get(code__exact=code, valid_from__lte=now, valid_to__gte=now, active=True)
                return coupon.discount
            except Coupon.DoesNotExist:
                raise ValueError("این کد تخفیف وجود ندارد!")
        return 0
