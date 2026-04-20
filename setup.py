import os
import subprocess

def run_command(cmd):
    """Run a command and print output"""
    print(f"\n>>> {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR: {result.stderr}")
        return False
    if result.stdout:
        print(result.stdout)
    return True

def main():
    print("=" * 50)
    print("EduPath Uganda Django Setup")
    print("=" * 50)
    
    # Step 1: Install requirements
    print("\n[1/5] Installing requirements...")
    run_command("py -m pip install -r requirements.txt")
    
    # Step 2: Create Django project
    print("\n[2/5] Creating Django project...")
    if not os.path.exists("manage.py"):
        run_command("py -m django startproject edupath .")
        print("✓ Django project created")
    else:
        print("✓ Django project already exists")
    
    # Step 3: Create apps
    print("\n[3/5] Creating Django apps...")
    apps = ["accounts", "schools", "students", "advertising"]
    for app in apps:
        if not os.path.exists(app):
            run_command(f"py manage.py startapp {app}")
            print(f"✓ Created {app} app")
        else:
            print(f"✓ {app} app already exists")
    
    # Step 4: Run initial migrations
    print("\n[4/5] Running database migrations...")
    run_command("py manage.py makemigrations")
    run_command("py manage.py migrate")
    print("✓ Database setup complete")
    
    # Step 5: Create superuser
    print("\n[5/5] Creating superuser...")
    print("Please create an admin account:")
    run_command("py manage.py createsuperuser")
    
    print("\n" + "=" * 50)
    print("✅ Setup Complete!")
    print("=" * 50)
    print("\nTo start the development server:")
    print("  py manage.py runserver")
    print("\nThen visit:")
    print("  http://127.0.0.1:8000/admin/")
    print("  http://127.0.0.1:8000/api/auth/meta/")
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()