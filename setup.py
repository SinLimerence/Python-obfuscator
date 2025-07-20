import sys
import subprocess
import importlib

STD_LIB_MODULES = {
    'ast', 'base64', 'zlib', 'random', 'string', 
    're', 'sys', 'marshal', 'io', 'collections'
}

EXTERNAL_PACKAGES = []  

def check_imports():
    print("=== Checking Python Standard Library Imports ===")
    all_success = True
    
    for module in STD_LIB_MODULES:
        try:
            importlib.import_module(module)
            print(f"✓ {module} (standard library)")
        except ImportError:
            print(f"✗ {module} (missing - this should never happen!)")
            all_success = False
    
    return all_success

def install_external_packages():
    if not EXTERNAL_PACKAGES:
        print("\nNo external packages need installation.")
        return True
    
    print(f"\nThe following external packages will be installed: {', '.join(EXTERNAL_PACKAGES)}")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + EXTERNAL_PACKAGES)
        print("External packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install packages. Error: {e}")
        return False

if __name__ == "__main__":
    print("=== Python Obfuscator Dependency Checker ===")
    
    std_lib_ok = check_imports()
    
    ext_packages_ok = install_external_packages()
    
    if std_lib_ok and ext_packages_ok:
        print("\nAll dependencies are available!")
        sys.exit(0)
    else:
        print("\nSome issues were encountered:")
        if not std_lib_ok:
            print("- Missing standard library modules (this is very unusual)")
        if not ext_packages_ok:
            print("- Failed to install external packages")
        print("\nPlease consult the error messages above.")
        sys.exit(1)