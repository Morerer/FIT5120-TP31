#!/usr/bin/env python3
"""
Quick database initialization script for Melbourne CBD Parking System
Run this once to set up your database with sample data.
"""

import os
import sys

def main():
    print(" Melbourne CBD Parking System - Database Setup")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print(" Please run this script from the same directory as main.py")
        sys.exit(1)
    
    # Create database directory if it doesn't exist
    os.makedirs("database", exist_ok=True)
    
    # Create __init__.py for database package
    init_file = "database/__init__.py"
    if not os.path.exists(init_file):
        with open(init_file, "w") as f:
            f.write("# Database package\n")
        print(" Created database package")
    
    try:
        # Import and run database setup
        print(" Setting up database...")
        from database.setup import main as setup_main
        setup_main()
        
        print("\n Database setup completed successfully!")
        print("\nNext Steps:")
        print("   1. Start FastAPI server: python main.py")
        print("   2. Visit API docs: http://localhost:8000/docs")
        print("   3. Test endpoints: http://localhost:8000/api/trends/population")
        print("   4. Update your React frontend to use the new API")
        
    except ImportError as e:
        print(f" Import error: {e}")
        print("Make sure you've saved the database models and setup files")
        sys.exit(1)
    except Exception as e:
        print(f"Setup error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()