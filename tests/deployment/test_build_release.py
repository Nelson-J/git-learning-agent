import pytest
import os
from unittest.mock import patch, MagicMock
import zipfile

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

@patch('subprocess.run')
def test_build_executable(mock_run):
    mock_run.return_value = MagicMock(returncode=0)
    result = build_executable()
    assert result is True
    assert mock_run.call_count == 2

@patch('zipfile.ZipFile')
def test_create_release_package(mock_zip, tmp_output_dir):
    version = "1.0.0"
    result = create_release_package(version, tmp_output_dir)
    assert result is True
    mock_zip.assert_called_once()
