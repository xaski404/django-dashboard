from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Task, Note
from .forms import TaskForm, NoteForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, f'Witaj, {form.get_user().username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Nieprawidłowy login lub hasło.')
    else:
        form = AuthenticationForm()
    return render(request, 'dashboard/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Konto utworzone! Witaj w Dashboard.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Popraw błędy w formularzu.')
    else:
        form = UserCreationForm()
    return render(request, 'dashboard/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    tasks = Task.objects.filter(user=request.user)
    notes = Note.objects.filter(user=request.user)

    # Stats
    total_tasks = tasks.count()
    done_tasks = tasks.filter(status='done').count()
    in_progress_tasks = tasks.filter(status='in_progress').count()
    todo_tasks = tasks.filter(status='todo').count()
    total_notes = notes.count()

    # Upcoming deadlines (next 7 days)
    today = timezone.now().date()
    upcoming = tasks.filter(
        due_date__gte=today,
        due_date__lte=today + timedelta(days=7),
        status__in=['todo', 'in_progress']
    ).order_by('due_date')[:5]

    # Recent tasks
    recent_tasks = tasks[:5]
    pinned_notes = notes.filter(pinned=True)[:4]

    context = {
        'total_tasks': total_tasks,
        'done_tasks': done_tasks,
        'in_progress_tasks': in_progress_tasks,
        'todo_tasks': todo_tasks,
        'total_notes': total_notes,
        'upcoming': upcoming,
        'recent_tasks': recent_tasks,
        'pinned_notes': pinned_notes,
        'completion_rate': round((done_tasks / total_tasks * 100) if total_tasks > 0 else 0),
    }
    return render(request, 'dashboard/index.html', context)


# --- TASK VIEWS ---

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)

    # Filters
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)

    context = {
        'tasks': tasks,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
    }
    return render(request, 'dashboard/task_list.html', context)


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Zadanie zostało dodane!')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'dashboard/task_form.html', {'form': form, 'title': 'Nowe zadanie'})


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Zadanie zaktualizowane!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'dashboard/task_form.html', {'form': form, 'title': 'Edytuj zadanie'})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Zadanie usunięte!')
    return redirect('task_list')


@login_required
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if task.status == 'done':
        task.status = 'todo'
    else:
        task.status = 'done'
    task.save()
    return redirect(request.META.get('HTTP_REFERER', 'task_list'))


# --- NOTE VIEWS ---

@login_required
def note_list(request):
    notes = Note.objects.filter(user=request.user)
    return render(request, 'dashboard/note_list.html', {'notes': notes})


@login_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, 'Notatka dodana!')
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'dashboard/note_form.html', {'form': form, 'title': 'Nowa notatka'})


@login_required
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notatka zaktualizowana!')
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'dashboard/note_form.html', {'form': form, 'title': 'Edytuj notatkę'})


@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Notatka usunięta!')
    return redirect('note_list')


@login_required
def note_toggle_pin(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    note.pinned = not note.pinned
    note.save()
    return redirect(request.META.get('HTTP_REFERER', 'note_list'))
