import pytest
import os
from scripts.build_release import clean_output_dir, build_executable, create_release_package

@pytest.fixture
def tmp_output_dir(tmp_path):
    """Create a temporary output directory for testing."""
    output_dir = str(tmp_path / "dist")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def test_clean_output_directory(tmp_output_dir):
    """Test cleaning output directory."""
    # Create some test files
    test_file = os.path.join(tmp_output_dir, "test.exe")
    with open(test_file, "w") as f:
        f.write("dummy content")
    
    clean_output_dir(tmp_output_dir)
    assert not os.path.exists(test_file)

def test_build_executable():
    """Test building executable."""
    result = build_executable()
    assert result is True
    assert os.path.exists(os.path.join("dist", "git-learning-system.exe"))

def test_create_release_package(tmp_output_dir):
    """Test creating release package."""
    version = "1.0.0"
    
    # Create a dummy executable for testing
    os.makedirs(os.path.join("dist"), exist_ok=True)
    with open(os.path.join("dist", "git-learning-system.exe"), "w") as f:
        f.write("dummy executable")
    
    result = create_release_package(version, tmp_output_dir)
    assert result is True
    assert os.path.exists(os.path.join(tmp_output_dir, f"git-learning-system-{version}.zip"))
