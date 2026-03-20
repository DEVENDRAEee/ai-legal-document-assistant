from django import forms
from .models import Document


class DocumentUploadForm(forms.ModelForm):
    """Form for uploading documents."""
    
    class Meta:
        model = Document
        fields = ['title', 'file']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a descriptive title for your document'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.docx,.jpg,.png,.txt'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['file'].required = True
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Check file size (10MB limit)
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError('File size must be less than 10MB.')
            
            # Check file type
            allowed_types = ['application/pdf', 
                           'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                           'image/jpeg', 'image/png', 'text/plain']
            
            if file.content_type not in allowed_types:
                raise forms.ValidationError('Please upload a PDF, DOCX, JPG, PNG, or TXT file.')
        
        return file


class ContactForm(forms.Form):
    """Contact form for user feedback."""
    
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your full name'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        })
    )
    
    subject = forms.ChoiceField(
        choices=[
            ('', 'Choose a subject'),
            ('general', 'General Inquiry'),
            ('technical', 'Technical Support'),
            ('feature', 'Feature Request'),
            ('bug', 'Bug Report'),
            ('feedback', 'Feedback'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Please describe your inquiry in detail...'
        })
    )
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError('Message must be at least 10 characters long.')
        return message