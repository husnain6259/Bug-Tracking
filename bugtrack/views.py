from django.db.models import Q
from bugtrack.models import Bug
from project.models import Project
from bugtrack.forms import BugForm 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest


@login_required(login_url='login')
def bugList(request, project_id):

    user_role = None
    if hasattr(request.user, 'role'):
        if request.user.role == 'qa':
             user_role = 'is_qa'
    # Get the project object
    project = get_object_or_404(Project, id=project_id)
    # Get the search query
    # Default empty string if 'q' is not provided
    query = request.GET.get('q', '')  
    if query:
        # Filter bugs based on the search query and project
        bugs = Bug.objects.filter(
            project=project
        ).filter(
            Q(status__icontains=query) |
            Q(description__icontains=query)
        )
        if bugs.exists():
            messages.info(request, "Search results found.")
        else:
            messages.info(request, "No search results found.")
    else:
        # If no query, get all bugs for the project
        bugs = Bug.objects.filter(project=project)
    total_bugs = bugs.count()
    assigned_bugs = bugs.filter(status='assigned').count()
    page_size = request.GET.get('page_size', 2) 
    paginator = Paginator(bugs, page_size)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Calculate the range for "Showing 1 to 2 entries"
    start_index = (page_obj.number - 1) * page_obj.paginator.per_page + 1
    end_index = start_index + len(page_obj.object_list) - 1
    context = {
        'project': project,
        'page_obj': page_obj,
        'page_size': page_size,
        'total_entries': paginator.count,
        'start_index': start_index,
        'end_index': end_index,
        'total_bugs': total_bugs,
        'assigned_bugs': assigned_bugs,
        'query': query,  # Pass the query back to the template
        'user_role': user_role,  # Pass user role to the template
    }
    return render(request, 'base/bug.html', context)


@login_required(login_url='login')
def addBug(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = BugForm(request.POST, request.FILES)
        if form.is_valid():
            bug = form.save(commit=False)
            bug.project = project 
            bug.save()
            return redirect('bug_list',project_id=project.id)
    else:
        form = BugForm()
    return render(request, 'base/bugadd.html', {'form': form, 'project': project})


def updateStatus(request, bug_id, status):
    bug = Bug.objects.get(id=bug_id)
    bug.status = status
    bug.save()
    messages.success(request, 'Bug status updated successfully!')
    return redirect('bug_list',project_id=bug.project.id)

def deleteBug(request, bug_id):
    bug = Bug.objects.get(id=bug_id)
    bug.delete()
    messages.success(request, 'Bug deleted successfully!')
    return redirect('bug_list',bug_id)


def updateDueDate(request, bug_id):
    bug = Bug.objects.get(id=bug_id)
    if request.method == 'GET':
        bug.due_date = request.GET.get('due_date')
        bug.save()
        return redirect('bug_list')
    


