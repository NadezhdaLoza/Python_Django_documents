from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'last_name', 'first_name', 'middle_name', 'post',
            'passport_series', 'passport_number',
            'passport_issued_by', 'passport_date_of_issue',
        ]
        widgets = {
            'passport_date_of_issue': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d',
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['passport_date_of_issue'].input_formats = ['%Y-%m-%d']
