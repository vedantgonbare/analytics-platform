import subprocess
import sys

if __name__ == "__main__":
    result = subprocess.run(
        ["alembic", "upgrade", "head"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    print(result.stderr)
    sys.exit(result.returncode)