from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Tournament, RegisteredTeams, Results


queryset = RegisteredTeams.objects.all()


class MyDateInput(forms.DateTimeInput):
    input_type = 'date'


class TournamentForm(forms.ModelForm):
    title = forms.CharField(label='', widget=forms.TextInput
                            (
                                attrs={
                                    'placeholder': 'Tournament Title',
                                    'class': 'form-control'
                                }
                            ))

    description = forms.CharField(
        label='', widget=CKEditorWidget(config_name='default'))

    prize_pool = forms.IntegerField(label='', widget=forms.NumberInput
                                    (
                                        attrs={
                                          'placeholder': 'Prize Pool',
                                            'class': 'form-control'
                                        }
                                    ))

    fee = forms.IntegerField(label='', required=False, widget=forms.NumberInput
                             (
                                 attrs={
                                   'placeholder': 'Registeration Fee',
                                     'class': 'form-control'
                                 }
                             ))

    slots = forms.IntegerField(label='', min_value=1, widget=forms.NumberInput
                               (
                                   attrs={
                                     'placeholder': 'Max Slots',
                                       'class': 'form-control'
                                   }
                               ))

    last_date = forms.DateTimeField(label='', widget=MyDateInput(
        attrs={
            'class': 'form-control'
        }
    ))

    class Meta:
        model = Tournament
        fields = [
            'title',
            'image',
            'description',
            'prize_pool',
            'fee',
            'slots',
            'last_date',
            'is_active',

        ]


class TeamsRegisterationForm(forms.ModelForm):
    team_name = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Team Name'
        }
    ))

    team_number = forms.IntegerField(label='', widget=forms.NumberInput(
        attrs={
            'placeholder': 'Whatsapp Number'
        }
    ))

    player1_ign = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Player 1 IGN'
        }
    ))

    player2_ign = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Player 2 IGN'
        }
    ))

    player3_ign = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Player 3 IGN'
        }
    ))

    player4_ign = forms.CharField(label='', widget=forms.TextInput(
        attrs={
            'placeholder': 'Player 4 IGN'
        }
    ))

    player5_ign = forms.CharField(label='', required=False, widget=forms.TextInput(
        attrs={
            'placeholder': 'Player 5 IGN'
        }
    ))

    class Meta:
        model = RegisteredTeams
        fields = [
            'team_name',
            'team_number',
            'player1_ign',


            'player2_ign',


            'player3_ign',


            'player4_ign',


            'player5_ign',


        ]
