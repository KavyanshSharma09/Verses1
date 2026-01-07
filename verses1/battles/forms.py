from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Battle, CodeSubmission, ProblemStatement

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class BattleCreationForm(forms.ModelForm):
    problem = forms.ModelChoiceField(
        queryset=ProblemStatement.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Select a problem...",
        help_text="Choose a problem for this battle"
    )
    
    class Meta:
        model = Battle
        fields = ['problem']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Group problems by difficulty
        self.fields['problem'].queryset = ProblemStatement.objects.filter(
            is_active=True
        ).order_by('difficulty', 'title')

class CodeSubmissionForm(forms.ModelForm):
    code_content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 20,
            'placeholder': 'Write your code here...',
            'style': 'font-family: monospace;'
        }),
        required=False,
        help_text='Write or paste your Python code here'
    )
    
    class Meta:
        model = CodeSubmission
        fields = ['code_content', 'code_file']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code_file'].required = False
        self.fields['code_file'].widget.attrs.update({'class': 'form-control'})
        self.fields['code_file'].help_text = 'Or upload a Python file (.py)'

    def clean(self):
        cleaned_data = super().clean()
        code_content = cleaned_data.get('code_content', '').strip()
        code_file = cleaned_data.get('code_file')
        
        if not code_content and not code_file:
            raise forms.ValidationError('Please either write code or upload a file.')
        
        if code_file and not code_file.name.endswith('.py'):
            raise forms.ValidationError('Only Python (.py) files are allowed.')
        
        # If file is uploaded, read its content
        if code_file and not code_content:
            cleaned_data['code_content'] = code_file.read().decode('utf-8')
            code_file.seek(0)  # Reset file pointer
        
        return cleaned_data

class BattleJoinForm(forms.Form):
    battle_code = forms.CharField(max_length=8, min_length=8,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter battle code'}))

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_battle_code(self):
        code = self.cleaned_data.get('battle_code')
        try:
            battle = Battle.objects.get(battle_code=code, is_completed=False)
            if battle.opponent is not None:
                raise forms.ValidationError('This battle is already full.')
            if self.user and battle.creator == self.user:
                raise forms.ValidationError('You cannot join your own battle.')
            return code
        except Battle.DoesNotExist:
            raise forms.ValidationError('Invalid battle code.')
