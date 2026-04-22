from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Niski'),
        ('medium', 'Średni'),
        ('high', 'Wysoki'),
    ]
    STATUS_CHOICES = [
        ('todo', 'Do zrobienia'),
        ('in_progress', 'W trakcie'),
        ('done', 'Zrobione'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200, verbose_name='Tytuł')
    description = models.TextField(blank=True, verbose_name='Opis')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name='Priorytet')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo', verbose_name='Status')
    due_date = models.DateField(null=True, blank=True, verbose_name='Termin')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Zadanie'
        verbose_name_plural = 'Zadania'

    def __str__(self):
        return self.title


class Note(models.Model):
    COLOR_CHOICES = [
        ('#6c5ce7', 'Fioletowy'),
        ('#00b894', 'Zielony'),
        ('#fdcb6e', 'Żółty'),
        ('#e17055', 'Pomarańczowy'),
        ('#0984e3', 'Niebieski'),
        ('#d63031', 'Czerwony'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200, verbose_name='Tytuł')
    content = models.TextField(verbose_name='Treść')
    color = models.CharField(max_length=7, choices=COLOR_CHOICES, default='#6c5ce7', verbose_name='Kolor')
    pinned = models.BooleanField(default=False, verbose_name='Przypięta')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-pinned', '-created_at']
        verbose_name = 'Notatka'
        verbose_name_plural = 'Notatki'

    def __str__(self):
        return self.title
