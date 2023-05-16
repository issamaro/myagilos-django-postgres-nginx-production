from django.forms import CharField, DateField, DateInput, Form, ModelForm, PasswordInput, TextInput, TypedChoiceField
from .models import Cases, Certifications, Consultant_certifications, ForgotPassword
from .custom_widgets import CustomSelect


class ForgotPasswordForm(ModelForm):
    class Meta:
        model = ForgotPassword
        fields = [
            "username",
            "email"
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"placeholder": "Enter your username"})
        self.fields["email"].widget.attrs.update({"placeholder": "Enter your email"})


class CasesForm(ModelForm):
    class Meta:
        model = Cases
        fields = [
            "industry",
            "company",
            "project_start",
            "project_end",
            "issue",
            "architecture",
            "challenge",
            "solution",
            "tools",
            "why_agilos",
            "gpt_content"
        ]
        labels = {
            "why_agilos": "Why Agilos",
            "project_start": "Start date",
            "project_end": "End date",
            "gpt_content": "GPT Content"
        }
        widgets = {
            "project_start": DateInput(attrs={"type": "date"}),
            "project_end": DateInput(attrs={"type": "date"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["company"].widget.attrs.update({"placeholder": "Select a company"})
        self.fields["issue"].widget.attrs.update({"placeholder": "What problem was the customer facing?"})
        self.fields["architecture"].widget.attrs.update({"placeholder": "What architecture was implemented before the project?"})
        self.fields["challenge"].widget.attrs.update({"placeholder": "What was the challenge with this project?"})
        self.fields["solution"].widget.attrs.update({"placeholder": "What was the provided solution? How did it help the customer?"})
        self.fields["tools"].widget.attrs.update({"placeholder": "Which tools did you use? For what reasons?"})
        self.fields["why_agilos"].widget.attrs.update({"placeholder": "For what reasons do you think the customer chose to work with Agilos?"})

    
    industry = TypedChoiceField(choices=Cases.INDUSTRIES, widget=CustomSelect)


class ResetPasswordForm(Form):
    username = CharField(label="Username", max_length=64, widget=TextInput(attrs={'placeholder': 'john.doe'}))
    password = CharField(label="New Password", widget=PasswordInput(attrs={'placeholder': 'New Password'}))


class AddCertificationForm(Form):
    # class Meta:
    #     model = Consultant_certifications
    #     fields = "__all__"

# class ConsultantCertificationForm(Form):
    company = CharField(max_length=64)
    title = CharField(max_length=254)
    earned_at = DateField()
    expires_at = DateField()
    certification_idcode = CharField(max_length=128)
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
    
    def save(self):
        # Get or create certification
        certification, created = Certifications.objects.get_or_create(
            company=self.cleaned_data['company'],
            title=self.cleaned_data['title']
        )
        
        # Create consultant certification
        consultant_certification = Consultant_certifications(
            consultant=self.request.user.as_consultant,
            certification=certification,
            earned_at=self.cleaned_data['earned_at'],
            expires_at=self.cleaned_data['expires_at'],
            certification_idcode=self.cleaned_data['certification_idcode']
        )
        consultant_certification.save()


