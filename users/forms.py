from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .models import EventType
from .models import State
from .models import Region

WEEKDAYS = [
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday')
]

DIST_FREQ = [
    (7, 'Weekly'),
    (14, 'BiWeekly'),
    (28, 'Monthly')
]

DISTRIBUTION = [
    (True, ' Email Distributions ON'),
    (False, ' Email Distribution OFF')
]


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email']


class ProfileForm(forms.ModelForm):

    zip = forms.CharField(
                          label='Of',
                          required=False,
                          max_length=5,
                          min_length=5,
                          widget=forms.TextInput(
                              attrs={
                                  'placeholder': "Zip"
                              }
                          )
                          )

    distance = forms.IntegerField(
                          label='Within',
                          min_value=0,
                          max_value=500,
                          required=False,
                          widget=forms.NumberInput(
                              attrs={
                                  'placeholder': "Miles"
                              }
                          )
                          )

    distrib = forms.ChoiceField(
                            label='Distribution Setting',
                            widget=forms.RadioSelect(),
                            choices=DISTRIBUTION)

    event = forms.MultipleChoiceField(
                            label='Event Types',
                            required=True,
                            widget=forms.CheckboxSelectMultiple(),
                            choices=tuple(EventType.objects.all().values_list())
                                        )

    region = forms.MultipleChoiceField(
                            label='Region',
                            required=False,
                            widget=forms.SelectMultiple(),
                            choices=tuple(Region.objects.all().values_list())
                                        )

    states = forms.MultipleChoiceField(
                            label='State',
                            required=False,
                            widget=forms.SelectMultiple(),
                            choices=tuple(State.objects.all().values_list())
                                        )

    dstr_cad = forms.ChoiceField(
                            label="Distribution Frequency",
                            required=True,
                            widget=forms.Select(
                                attrs={
                                    'class': 'custom-select'
                                }
                            ),
                            choices=DIST_FREQ
                                )

    dstr_day = forms.ChoiceField(
                            label="Distribution Day",
                            required=True,
                            widget=forms.Select(
                                attrs={
                                    'class': 'custom-select'
                                }
                            ),
                            choices=WEEKDAYS
                                )

    class Meta:
        model = Profile
        fields = [
            'zip', 'distance', 'region', 'states', 'event',
            'dstr_cad', 'dstr_day', 'location', 'distrib', 'run_date'
           ]

    def clean(self):
        cleaned_data = super().clean()
        zip = cleaned_data.get("zip")
        state_pk = [i for i in cleaned_data.get('states')]
        region_pk = [i for i in cleaned_data.get('region')]
        distance = cleaned_data.get("distance")
	#below region and state are null vals--did not want to reset pk indexing at this time
        if (not distance or not zip) and (not region_pk or region_pk == ['10']) and (not state_pk or state_pk == ['157']):
            raise forms.ValidationError(
                    "Please use either distance from zip or state or region options."
                )

