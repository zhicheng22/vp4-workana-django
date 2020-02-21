from django import forms
from register.models import BaseUser
from .models import Complaint_Model, Category, Type

class Profile_Edit_Form(forms.ModelForm):
    class Meta:
        model = BaseUser
        fields = ['mobile_number', 'house_number', 'street_address', 'subdivision', 'city', 'zip_code',
                  'logo_cover']

class Create_Complaint_Form(forms.ModelForm):
    class Meta:
        model = Complaint_Model
        fields = ['respondent_first_name', 'respondent_last_name', 'respondent_address', 'category', 'type', 'subject', 'complain']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].queryset = Type.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['type'].queryset = Type.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['type'].queryset = self.instance.category.type_set.order_by('name')