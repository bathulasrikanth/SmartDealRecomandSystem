from django import forms

PURPOSE_CHOICES = [
    ('urgent','Urgent'),
    ('casual','Casual'),
    ('work','Work'),
    ('shopping','Shopping'),
]

COMPANY_CHOICES = [
    ('alone','Alone'),
    ('friends','Friends'),
    ('family','Family'),
]

WEATHER_CHOICES = [
    ('sunny','Sunny'),
    ('rainy','Rainy'),
    ('cloudy','Cloudy'),
    ('snowy','Snowy'),
]

class PredictForm(forms.Form):
    trip_purpose = forms.ChoiceField(choices=PURPOSE_CHOICES)
    travel_company = forms.ChoiceField(choices=COMPANY_CHOICES)
    current_weather = forms.ChoiceField(choices=WEATHER_CHOICES)
    temperature = forms.FloatField()
    age = forms.IntegerField(min_value=12, max_value=120)
    previous_redemption = forms.IntegerField(min_value=0, max_value=1, initial=0)
