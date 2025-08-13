#!/usr/bin/env python3
"""
Test runner script for the Group Fitness API

Usage:
    python run_tests.py                    # Run all tests
    python run_tests.py --unit             # Run only unit tests
    python run_tests.py --integration      # Run only integration tests
    python run_tests.py --auth             # Run only auth tests
    python run_tests.py --users            # Run only user tests
    python run_tests.py --group-events     # Run only group events tests
    python run_tests.py --coverage         # Run with coverage report
    python run_tests.py --verbose          # Run with verbose output
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_tests(args):
    """Run pytest with the given arguments"""
    cmd = ["python", "-m", "pytest"]
    
    # Add test path
    cmd.append("tests/")
    
    # Add markers based on arguments
    if args.unit:
        cmd.extend(["-m", "unit"])
    elif args.integration:
        cmd.extend(["-m", "integration"])
    elif args.auth:
        cmd.extend(["-m", "auth"])
    elif args.users:
        cmd.extend(["-m", "users"])
    elif args.group_events:
        cmd.extend(["-m", "group_events"])
    
    # Add coverage if requested
    if args.coverage:
        cmd.extend(["--cov=app", "--cov-report=html", "--cov-report=term"])
    
    # Add verbose output if requested
    if args.verbose:
        cmd.append("-v")
    
    # Add additional pytest arguments
    if args.pytest_args:
        cmd.extend(args.pytest_args)
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"Tests failed with exit code: {e.returncode}")
        return e.returncode


def main():
    parser = argparse.ArgumentParser(description="Run tests for Group Fitness API")
    
    # Test type options
    test_group = parser.add_mutually_exclusive_group()
    test_group.add_argument("--unit", action="store_true", help="Run only unit tests")
    test_group.add_argument("--integration", action="store_true", help="Run only integration tests")
    test_group.add_argument("--auth", action="store_true", help="Run only auth tests")
    test_group.add_argument("--users", action="store_true", help="Run only user tests")
    test_group.add_argument("--group-events", action="store_true", help="Run only group events tests")
    
    # Other options
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("pytest_args", nargs=argparse.REMAINDER, help="Additional pytest arguments")
    
    args = parser.parse_args()
    
    # Check if we're in the right directory
    if not Path("tests").exists():
        print("Error: tests directory not found. Make sure you're running this from the backend directory.")
        sys.exit(1)
    
    # Run the tests
    exit_code = run_tests(args)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
