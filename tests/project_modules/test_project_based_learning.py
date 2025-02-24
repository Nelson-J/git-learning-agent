import pytest
from git_learning_system.project_modules.project_based_learning import (
    ProjectBasedLearning,
    ProjectStatus,
    ProjectScenario,
    Milestone
)

@pytest.fixture
def pbl_instance():
    return ProjectBasedLearning()

def test_project_initialization(pbl_instance):
    """Test that projects are properly initialized"""
    assert len(pbl_instance.projects) > 0
    assert "website-version-control" in pbl_instance.projects
    assert "team-collaboration" in pbl_instance.projects

def test_get_existing_project(pbl_instance):
    """Test retrieving an existing project"""
    project = pbl_instance.get_project("website-version-control")
    assert project is not None
    assert project.name == "Website Version Control"
    assert project.difficulty == 1
    assert len(project.milestones) == 3

def test_get_nonexistent_project(pbl_instance):
    """Test retrieving a non-existent project"""
    project = pbl_instance.get_project("nonexistent-project")
    assert project is None

def test_update_milestone(pbl_instance):
    """Test milestone update functionality"""
    # Test successful update
    result = pbl_instance.update_milestone("website-version-control", "init", True)
    assert result is True
    
    project = pbl_instance.get_project("website-version-control")
    assert project.milestones[0].completed is True

    # Test update with invalid milestone
    result = pbl_instance.update_milestone("website-version-control", "invalid-milestone", True)
    assert result is False

def test_project_status(pbl_instance):
    """Test project status retrieval"""
    status = pbl_instance.get_project_status("website-version-control")
    assert status == ProjectStatus.NOT_STARTED

    # Test non-existent project
    status = pbl_instance.get_project_status("nonexistent-project")
    assert status is None

def test_project_completion_check(pbl_instance):
    """Test project completion verification"""
    # Initially not completed
    assert pbl_instance.check_project_completion("website-version-control") is False

    # Complete all milestones
    project = pbl_instance.get_project("website-version-control")
    for milestone in project.milestones:
        pbl_instance.update_milestone("website-version-control", milestone.id, True)

    # Should now be completed
    assert pbl_instance.check_project_completion("website-version-control") is True

def test_project_difficulty_levels(pbl_instance):
    """Test that projects have appropriate difficulty levels"""
    web_project = pbl_instance.get_project("website-version-control")
    team_project = pbl_instance.get_project("team-collaboration")
    
    assert web_project.difficulty < team_project.difficulty
    assert web_project.difficulty == 1
    assert team_project.difficulty == 2

def test_collaboration_requirements(pbl_instance):
    """Test collaboration requirements are properly set"""
    web_project = pbl_instance.get_project("website-version-control")
    team_project = pbl_instance.get_project("team-collaboration")
    
    assert web_project.collaboration_required is False
    assert team_project.collaboration_required is True
