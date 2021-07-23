from django.forms import ModelForm, TimeInput,  DateInput
from .models import Game

class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['round', 'home', 'away', 'place', 'referee', 'time', 'ot_time', 'data', 'hour']
        widgets = {
            'data': DateInput(attrs={'type': 'date'}),
            'hour': TimeInput(attrs={'type': 'time'}),
        }
        labels = {
            'time': 'Quarter length (seconds)',
            'ot_time': 'OT length (seconds)',
            'hour': 'Game start'
        }