# Project Manager CLI

A simple command-line tool to manage users, projects, and tasks with JSON-based storage and rich terminal output.

## Features

- ✅ Create users
- ✅ Add projects to users
- ✅ Add tasks to projects
- ✅ Mark tasks as completed
- ✅ Delete tasks
- ✅ List all users, projects, and tasks
- ✅ Styled terminal output using `rich`

## Setup

Install required package:

```bash
pip install rich


```

## Commands

Create a user - python3 main.py create-user "name"

Add project to user - python3 main.py add-project 1 "my project"

Add task to project - python3 main.py add-task 1 1 "Do the thing"

Mark task complete - python3 main.py complete-task 1 1 1

Delete a task - python3 main.py delete-task 1 1 1

list all users, projects and tasks - python3 main.py list

RUN pytests tests for feature tests

## Data

Sotred locally to data.json
