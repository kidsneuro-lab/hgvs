# Used by Packager.Dockerfile to update the version in pyproject.toml
import toml
import sys

def update_version(version):
    with open("pyproject.toml", "r") as file:
        data = toml.load(file)
    
    data["project"]["version"] = version
    
    with open("pyproject.toml", "w") as file:
        toml.dump(data, file)
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python update_version.py <new_version>")
        sys.exit(1)
    
    new_version = sys.argv[1]
    update_version(new_version)