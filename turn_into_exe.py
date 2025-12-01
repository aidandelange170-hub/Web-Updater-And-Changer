import os
import subprocess
import sys

def create_exe():
    """
    Convert main_minimal.py into an executable using PyInstaller
    """
    # Change to the web_scraper directory
    scraper_dir = os.path.join(os.path.dirname(__file__), "web_scraper")
    if not os.path.exists(scraper_dir):
        print(f"Error: web_scraper directory not found at {scraper_dir}")
        return False
    
    main_py_path = os.path.join(scraper_dir, "main_minimal.py")
    print(f"Converting {main_py_path} to executable...")
    
    # Check if main_minimal.py exists
    if not os.path.exists(main_py_path):
        print(f"Error: main_minimal.py not found at {main_py_path}")
        return False
    
    # Install PyInstaller if not already installed
    try:
        import PyInstaller
        print("PyInstaller is already installed.")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Change to the scraper directory to run PyInstaller
    original_dir = os.getcwd()
    os.chdir(scraper_dir)
    
    try:
        # Run PyInstaller to create executable
        print("Creating executable...")
        result = subprocess.run([
            sys.executable, "-m", "PyInstaller",
            "--onefile",  # Create a single executable file
            "--name", "WebScraperMinimal",  # Name of the executable
            "--distpath", os.path.join(os.pardir, "dist"),  # Output to parent 'dist' directory
            "main_minimal.py"
        ])
        
        if result.returncode == 0:
            print("Executable created successfully in the 'dist' folder!")
            print("You can find your executable at: ../dist/WebScraperMinimal")
            print("\nNote: This is a minimal version of the web scraper that includes core functionality.")
            print("Usage: ./dist/WebScraperMinimal <URL> --output <output_file>")
            return True
        else:
            print("Error creating executable.")
            return False
    finally:
        # Change back to original directory
        os.chdir(original_dir)

if __name__ == "__main__":
    create_exe()