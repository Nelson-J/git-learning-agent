"""
Build script for creating GitHub Releases.

This script packages the Git Learning System for distribution via GitHub Releases.
"""

import os
import sys
import shutil
import logging
import argparse
import subprocess
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def parse_args():
    """
    Parse command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(description="Build script for GitHub Releases")
    
    parser.add_argument(
        "--version",
        help="Version number for the release",
        required=True
    )
    
    parser.add_argument(
        "--output-dir",
        help="Output directory for the release files",
        default="dist"
    )
    
    parser.add_argument(
        "--clean",
        help="Clean output directory before building",
        action="store_true"
    )
    
    return parser.parse_args()

def clean_output_dir(output_dir):
    """
    Clean output directory.
    
    Args:
        output_dir (str): Output directory path
    """
    if os.path.exists(output_dir):
        logger.info(f"Cleaning output directory: {output_dir}")
        shutil.rmtree(output_dir)
    
    os.makedirs(output_dir, exist_ok=True)

def build_executable():
    """
    Build executable using PyInstaller.
    
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info("Building executable with PyInstaller")
    
    try:
        # Check if PyInstaller is installed
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "pyinstaller"],
            check=True
        )
        
        # Build executable
        subprocess.run(
            [
                sys.executable,
                "-m",
                "PyInstaller",
                "--onefile",
                "--name",
                "git-learning-system",
                "src/main.py"
            ],
            check=True
        )
        
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to build executable: {str(e)}")
        return False

def create_release_package(version, output_dir):
    """
    Create release package.
    
    Args:
        version (str): Version number
        output_dir (str): Output directory path
        
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Creating release package for version {version}")
    
    try:
        # Create release directory
        release_dir = os.path.join(output_dir, f"git-learning-system-{version}")
        os.makedirs(release_dir, exist_ok=True)
        
        # Copy executable
        executable_path = os.path.join("dist", "git-learning-system.exe")
        if os.path.exists(executable_path):
            shutil.copy(executable_path, release_dir)
        else:
            logger.error(f"Executable not found: {executable_path}")
            return False
        
        # Copy README and LICENSE
        for file in ["README.md", "LICENSE"]:
            if os.path.exists(file):
                shutil.copy(file, release_dir)
        
        # Create version file
        with open(os.path.join(release_dir, "version.txt"), "w") as f:
            f.write(version)
        
        # Create zip archive
        shutil.make_archive(
            os.path.join(output_dir, f"git-learning-system-{version}"),
            "zip",
            output_dir,
            f"git-learning-system-{version}"
        )
        
        logger.info(f"Release package created: {os.path.join(output_dir, f'git-learning-system-{version}.zip')}")
        
        return True
    except Exception as e:
        logger.error(f"Failed to create release package: {str(e)}")
        return False

def main():
    """
    Main entry point.
    """
    args = parse_args()
    
    # Clean output directory if requested
    if args.clean:
        clean_output_dir(args.output_dir)
    
    # Build executable
    if not build_executable():
        logger.error("Failed to build executable")
        return 1
    
    # Create release package
    if not create_release_package(args.version, args.output_dir):
        logger.error("Failed to create release package")
        return 1
    
    logger.info("Release package created successfully")
    return 0

if __name__ == "__main__":
    sys.exit(main())
