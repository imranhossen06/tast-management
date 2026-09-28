from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Task


@login_required
def task_list(request):

    tasks = Task.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'tasks/task_list.html',
        {'tasks': tasks}
    )


@login_required
def task_detail(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk,
        user=request.user
    )

    return render(
        request,
        'tasks/task_detail.html',
        {'task': task}
    )


@login_required
def task_create(request):

    if request.method == 'POST':

        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')

        Task.objects.create(
            user=request.user,
            title=title,
            description=description,
            status=status
        )

        messages.success(request, 'Task created successfully.')
        return redirect('task_list')

    return render(request, 'tasks/task_form.html')


@login_required
def task_update(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':

        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.status = request.POST.get('status')

        task.save()

        messages.success(request, 'Task updated successfully.')
        return redirect('task_list')

    return render(
        request,
        'tasks/task_form.html',
        {'task': task}
    )


@login_required
def task_delete(request, pk):

    task = get_object_or_404(
        Task,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':
        task.delete()

        messages.success(request, 'Task deleted successfully.')
        return redirect('task_list')

    return render(
        request,
        'tasks/task_confirm_delete.html',
        {'task': task}
    )