import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import User, Project, Task

def test_create_task():
    task = Task(id=1, description="Test task")
    assert task.id == 1
    assert task.description == "Test task"
    assert task.completed is False

def test_create_project_and_add_task():
    project = Project(id=1, title="Demo Project")
    task = Task(id=1, description="Task in project")
    project.add_task(task)
    assert len(project.tasks) == 1
    assert project.tasks[0].description == "Task in project"

def test_create_user_and_add_project():
    user = User(id=1, name="Test User")
    project = Project(id=1, title="Test Project")
    user.add_project(project)
    assert len(user.projects) == 1
    assert user.projects[0].title == "Test Project"

def test_task_completion_toggle():
    task = Task(id=1, description="Complete this")
    assert not task.completed
    task.completed = True
    assert task.completed

def test_task_description_validation():
    try:
        Task(id=1, description="")
        assert False, "Expected ValueError for empty description"
    except ValueError:
        assert True