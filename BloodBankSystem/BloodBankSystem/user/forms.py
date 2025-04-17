from django import forms
from user.models import BloodRequest
from donor.models import DonorProfile

class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = [
            'requester_name', 'requester_email', 'requester_phone', 
            'patient_name', 'patient_age', 'patient_gender',
            'blood_group', 'units_required', 'hospital_name',
            'hospital_address', 'city', 'state', 'reason', 'needed_by_date'
        ]
        widgets = {
            'needed_by_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
            'hospital_address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super(BloodRequestForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class DonorSearchForm(forms.Form):
    blood_group = forms.ChoiceField(
        choices=[('', 'Select Blood Group')] + list(DonorProfile._meta.get_field('blood_group').choices),
        required=False
    )
    city = forms.CharField(max_length=100, required=False)
    
    def __init__(self, *args, **kwargs):
        super(DonorSearchForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class BloodRequestUpdateForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['status', 'remarks']
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super(BloodRequestUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
