from django import forms
from donor.models import DonorProfile
from django.contrib.auth.models import User
from accounts.forms import UserRegisterForm

class DonorRegistrationForm(UserRegisterForm):
    blood_group = forms.ChoiceField(choices=DonorProfile._meta.get_field('blood_group').choices)
    age = forms.IntegerField(min_value=18, max_value=65)
    gender = forms.ChoiceField(choices=DonorProfile._meta.get_field('gender').choices)
    phone_number = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    
    class Meta(UserRegisterForm.Meta):
        model = User
        fields = UserRegisterForm.Meta.fields + ['blood_group', 'age', 'gender', 'phone_number', 'address', 'city', 'state']

class DonorProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = DonorProfile
        fields = ['profile_pic', 'blood_group', 'age', 'gender', 'phone_number', 'address', 'city', 'state', 'medical_history', 'is_available']
        widgets = {
            'medical_history': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super(DonorProfileUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['is_available'].widget.attrs.update({'class': 'form-check-input'})
        if 'profile_pic' in self.fields:
            self.fields['profile_pic'].widget.attrs.update({'class': 'form-control-file'})
