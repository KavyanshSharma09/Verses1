from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Battle, CodeSubmission

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class BattleCreationForm(forms.ModelForm):
    class Meta:
        model = Battle
        fields = []

class CodeSubmissionForm(forms.ModelForm):
    class Meta:
        model = CodeSubmission
        fields = ['code_file']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code_file'].widget.attrs.update({'class': 'form-control'})
        self.fields['code_file'].help_text = 'Upload your Python file here (.py files only)'

    def clean_code_file(self):
        code_file = self.cleaned_data.get('code_file')
        if not code_file.name.endswith('.py'):
            raise forms.ValidationError('Only Python (.py) files are allowed.')
        return code_file

class BattleJoinForm(forms.Form):
    battle_code = forms.CharField(max_length=8, min_length=8,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter battle code'}))

    def clean_battle_code(self):
        code = self.cleaned_data.get('battle_code')
        try:
            battle = Battle.objects.get(battle_code=code, is_completed=False)
            if battle.opponent is not None:
                raise forms.ValidationError('This battle is already full.')
            return code
        except Battle.DoesNotExist:
            raise forms.ValidationError('Invalid battle code.')
