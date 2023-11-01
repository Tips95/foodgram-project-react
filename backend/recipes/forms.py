from django import forms
from .models import Tag


class TagForm(forms.ModelForm):
    """Форма для создания и обновления тегов."""

    class Meta:
        model = Tag
        fields = ['name', 'color']

    COLOR_CHOICES = [
        ('#FF5733', 'Red'),
        ('#33FF57', 'Green'),
        ('#5733FF', 'Blue'),
        ('#FF33C6', 'Pink'),
        ('#33C6FF', 'Cyan'),
        ('#FFFF33', 'Yellow'),
    ]

    color = forms.ChoiceField(choices=COLOR_CHOICES, widget=forms.Select(
        attrs={'class': 'form-control'}))
