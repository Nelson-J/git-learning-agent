from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class ProjectStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

@dataclass
class Milestone:
    id: str
    description: str
    requirements: List[str]
    completed: bool = False

@dataclass
class ProjectScenario:
    id: str
    name: str
    description: str
    difficulty: int
    milestones: List[Milestone]
    collaboration_required: bool
    status: ProjectStatus = ProjectStatus.NOT_STARTED

class ProjectBasedLearning:
    def __init__(self):
        self.projects: Dict[str, ProjectScenario] = self._initialize_projects()
        
    def _initialize_projects(self) -> Dict[str, ProjectScenario]:
        return {
            "website-version-control": ProjectScenario(
                id="web-001",
                name="Website Version Control",
                description="Manage a small website project using Git",
                difficulty=1,
                collaboration_required=False,
                milestones=[
                    Milestone("init", "Initialize the repository", ["git init"]),
                    Milestone("first-commit", "Add HTML files", ["git add", "git commit"]),
                    Milestone("feature-branch", "Create a new feature branch", ["git branch", "git checkout"]),
                ]
            ),
            "team-collaboration": ProjectScenario(
                id="team-001",
                name="Team Collaboration Project",
                description="Work on a shared codebase with simulated team members",
                difficulty=2,
                collaboration_required=True,
                milestones=[
                    Milestone("clone", "Clone the team repository", ["git clone"]),
                    Milestone("feature", "Develop new feature", ["git branch", "git push"]),
                    Milestone("review", "Review and merge changes", ["git pull", "git merge"]),
                ]
            )
        }

    def get_project(self, project_id: str) -> Optional[ProjectScenario]:
        return self.projects.get(project_id)

    def update_milestone(self, project_id: str, milestone_id: str, completed: bool) -> bool:
        project = self.projects.get(project_id)
        if not project:
            return False
        
        for milestone in project.milestones:
            if milestone.id == milestone_id:
                milestone.completed = completed
                return True
        return False

    def get_project_status(self, project_id: str) -> Optional[ProjectStatus]:
        project = self.projects.get(project_id)
        if not project:
            return None
        return project.status

    def check_project_completion(self, project_id: str) -> bool:
        project = self.projects.get(project_id)
        if not project:
            return False
        return all(milestone.completed for milestone in project.milestones)
