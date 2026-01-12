#!/usr/bin/env python3
"""
Test runner script for Honda Vehicle API
"""

import subprocess
import sys
import os

def run_tests():
    """Run the test suite with coverage"""
    
    # Change to project directory
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_dir)
    
    print("🧪 Running Honda Vehicle API Test Suite")
    print("=" * 50)
    
    # Run tests with coverage
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--cov=app",
        "--cov-report=html",
        "--cov-report=term-missing",
        "--color=yes"
    ]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n✅ All tests passed!")
        print("📊 Coverage report generated in htmlcov/")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code {e.returncode}")
        return e.returncode
    except FileNotFoundError:
        print("❌ pytest not found. Please install dependencies:")
        print("pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
