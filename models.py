#parent for inheritance 
class BaseModel:
    def __init__(self,id):
        self.id = id


    def to_dict(self):
        raise NotImplementedError("Subclasses must implement to_dict method")




class Task(BaseModel):
    _id_counter = 1

    def __init__(self, id, description, completed=False):
        super().__init__(id)
        self.description = description
        self.completed = completed

    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value):
        if not value:
            raise ValueError("Description cannot be empty.")
        self._description = value

    @property
    def completed(self):
        return self._completed
    
    @completed.setter
    def completed(self, value):
        self._completed = bool(value)

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "completed": self.completed
        }
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            description=data["description"],
            completed=data.get("completed", False)
        )
    
    def __repr__(self):
        status = "Done" if self.completed else "Pending"
        return f"Task(id={self.id}, description='{self.description}', status={status})"

  


class Project(BaseModel):
    _id_counter = 1

    def __init__(self, id, title):
        super().__init__(id)
        self.title = title
        self.tasks = []

   
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value:
            raise ValueError("Project title cannot be empty.")
        self._title = value

    def add_task(self, task):
        self.tasks.append(task)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "tasks": [task.to_dict() for task in self.tasks]
        }

    @classmethod
    def from_dict(cls, data):
        project = cls(id=data["id"], title=data["title"])
        from models import Task  # prevents circular import
        project.tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
        return project

    def __repr__(self):
        return f"Project(id={self.id}, title='{self.title}', tasks={len(self.tasks)})"


class User(BaseModel):
    _id_counter = 1

    def __init__(self, id, name):
        super().__init__(id)
        self.name = name
        self.projects = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("User name cannot be empty.")
        self._name = value

    def add_project(self, project):
        self.projects.append(project)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "projects": [p.to_dict() for p in self.projects]
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(id=data["id"], name=data["name"])
        from models import Project
        user.projects = [Project.from_dict(p) for p in data.get("projects", [])]
        return user

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', projects={len(self.projects)})"