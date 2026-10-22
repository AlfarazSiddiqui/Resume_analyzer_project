from django import forms
from .models import Resume


class ResumeUploadForm(forms.ModelForm):
    job_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control', 'rows': 6,
            'placeholder': 'Paste the job description here for a tailored match score (optional but recommended)...'
        }),
    )

    class Meta:
        model = Resume
        fields = ['file', 'job_description']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.pdf,.docx,.txt'}),
        }

    def clean_file(self):
        file = self.cleaned_data['file']
        if file.size > 5 * 1024 * 1024:
            raise forms.ValidationError("File too large — please keep it under 5MB.")
        ext = file.name.split('.')[-1].lower()
        if ext not in ('pdf', 'docx', 'txt'):
            raise forms.ValidationError("Unsupported format. Please upload a PDF, DOCX, or TXT file.")
        return file
