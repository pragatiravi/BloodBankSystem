from django import forms
from bbadmin.models import BloodGroup, AdminProfile, ContactQuery
from django.contrib.auth.models import User
from accounts.forms import UserRegisterForm

class BloodGroupForm(forms.ModelForm):
    class Meta:
        model = BloodGroup
        fields = ['name', 'description', 'total_units']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super(BloodGroupForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class AdminRegistrationForm(UserRegisterForm):
    phone_number = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    
    class Meta(UserRegisterForm.Meta):
        model = User
        fields = UserRegisterForm.Meta.fields + ['phone_number', 'address']

class AdminProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = AdminProfile
        fields = ['profile_pic', 'phone_number', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super(AdminProfileUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        if 'profile_pic' in self.fields:
            self.fields['profile_pic'].widget.attrs.update({'class': 'form-control-file'})

class ContactResponseForm(forms.ModelForm):
    class Meta:
        model = ContactQuery
        fields = ['response']
        widgets = {
            'response': forms.Textarea(attrs={'rows': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        super(ContactResponseForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
