from django import forms
from django.forms import inlineformset_factory
from .models import TransferOrder, TransferOrderItem


class TransferOrderForm(forms.ModelForm):
    class Meta:
        model = TransferOrder
        fields = ['organization', 'document_number', 'document_date']
        widgets = {
            'document_date': forms.DateInput(attrs={'type': 'date'}),
        }


class TransferOrderItemForm(forms.ModelForm):
    class Meta:
        model = TransferOrderItem
        fields = [
            'employee', 'tab_number',
            'old_department', 'new_department',
            'old_position', 'new_position',
            'old_salary', 'new_salary',
            'transfer_type', 'date_from', 'date_to',
            'basis_document', 'basis_date'
        ]
        widgets = {
            'date_from': forms.DateInput(attrs={'type': 'date'}),
            'date_to': forms.DateInput(attrs={'type': 'date'}),
            'basis_date': forms.DateInput(attrs={'type': 'date'}),
        }


TransferOrderItemFormSet = inlineformset_factory(
    TransferOrder,
    TransferOrderItem,
    form=TransferOrderItemForm,
    extra=1,
    can_delete=True
)