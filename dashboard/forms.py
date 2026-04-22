from django import forms
from .models import Task, Note


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'status', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nazwa zadania...',
                'id': 'task-title-input',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input form-textarea',
                'placeholder': 'Opis zadania (opcjonalnie)...',
                'rows': 3,
                'id': 'task-description-input',
            }),
            'priority': forms.Select(attrs={
                'class': 'form-input form-select',
                'id': 'task-priority-select',
            }),
            'status': forms.Select(attrs={
                'class': 'form-input form-select',
                'id': 'task-status-select',
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
                'id': 'task-due-date-input',
            }),
        }


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'color', 'pinned']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Tytuł notatki...',
                'id': 'note-title-input',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-input form-textarea',
                'placeholder': 'Treść notatki...',
                'rows': 4,
                'id': 'note-content-input',
            }),
            'color': forms.Select(attrs={
                'class': 'form-input form-select',
                'id': 'note-color-select',
            }),
            'pinned': forms.CheckboxInput(attrs={
                'class': 'form-checkbox',
                'id': 'note-pinned-checkbox',
            }),
        }
