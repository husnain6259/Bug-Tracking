from django.shortcuts import render, redirect
from bugtrack.models import Bug
from project.models import Project
from project.forms import  ProjectForm 
from user.forms import LoginForm ,SignUpForm
from user.models import User 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

# yeh mein page pr sab kuch display krwa rha ha is liye yeh project mein aye ga
@login_required(login_url='login')

def index(request):
    query = request.GET.get('q')
    page_size = request.GET.get('page_size', 5)  # Default page size is 5
    page_number = request.GET.get('page', 1)  # Default to first page

    # Check user role (assuming role is stored in the user profile or model)
    user_role = None
    if hasattr(request.user, 'role'):
        if request.user.role == 'manager':
            user_role = 'is_manager'
        # elif request.user.role == 'qa':
        #     user_role = 'is_qa'
        elif request.user.role == 'developer':
            user_role = 'is_developer'

    # Search functionality
    if query:
        projects = Project.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
        if projects.exists():
            messages.info(request, "Search found.")
        else:
            messages.warning(request, "No search results found.")
    else:
        projects = Project.objects.all()

    # Collect project data with bug progress
    project_data = []
    for project in projects:
        total_bugs = Bug.objects.filter(project=project).count()
        completed_bugs = Bug.objects.filter(project=project, status='Completed').count()
        project_data.append({
            'project': project,
            'total_bugs': total_bugs,
            'completed_bugs': completed_bugs,
        })

    # Pagination setup
    paginator = Paginator(project_data, page_size)
    page_obj = paginator.get_page(page_number)

    # Start and end index for current page
    start_index = (page_obj.number - 1) * page_obj.paginator.per_page + 1
    end_index = start_index + len(page_obj.object_list) - 1

    # Context for the template
    context = {
        'page_obj': page_obj,
        'page_size': page_size,
        'total_entries': paginator.count,
        'start_index': start_index,
        'end_index': end_index,
        'user_role': user_role,  # Pass user role to the template
    }

    return render(request, 'base/index.html', context)


# add new project ka 
@login_required(login_url='login')
def addProject(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProjectForm()
    return render(request, 'base/project_add.html', {'form': form})


def deleteProject(request, pk):
    project = Project.objects.get(id=pk)
    if request.user.role == 'Manager':
        if request.method == 'POST':
            project.delete()
            return redirect('index')
        return render(request, 'base/project_delete.html', {'obj': project})
    else:
        return render(request, 'base/access_denied.html')


# For update the Project
def updateProject(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=project.id)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'base/project_update.html', {'form': form, 'project': project})


def projectDetail(request, project_id):
    project = Project.objects.get(id=project_id)
    return render(request, 'project_detail.html', {'project': project})

