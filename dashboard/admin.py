from django.contrib import admin
from .models import Task, Note


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'priority', 'status', 'due_date', 'created_at']
    list_filter = ['status', 'priority', 'user']
    search_fields = ['title', 'description']


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'color', 'pinned', 'created_at']
    list_filter = ['pinned', 'color', 'user']
    search_fields = ['title', 'content']
