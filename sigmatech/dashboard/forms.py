from django import forms
from order.models import Order

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']  # Only allow updating the status field
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }