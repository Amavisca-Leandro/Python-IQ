"""
Script to help Test Explorer discover BDD tests.

This script can be run to verify that pytest can discover all tests,
which should help the Test Explorer refresh its test list.
"""

import subprocess
import sys

def main():
    """Run pytest test discovery and display results."""
    print("=" * 70)
    print("DISCOVERING TESTS FOR TEST EXPLORER")
    print("=" * 70)
    print()
    
    # Run pytest collection
    print("Running: pytest --collect-only tests/bdd/ -q")
    print()
    
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "tests/bdd/", "-q"],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    
    print()
    print("=" * 70)
    
    if result.returncode == 0:
        print("✅ SUCCESS: Tests discovered successfully!")
        print()
        print("Next steps:")
        print("1. In Kiro IDE, open Command Palette (Ctrl+Shift+P)")
        print("2. Type: 'Test: Refresh Tests'")
        print("3. Press Enter")
        print()
        print("Or simply reload the window:")
        print("1. Command Palette (Ctrl+Shift+P)")
        print("2. Type: 'Developer: Reload Window'")
        print("3. Press Enter")
    else:
        print("❌ ERROR: Test discovery failed!")
        print(f"Return code: {result.returncode}")
    
    print("=" * 70)
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())
