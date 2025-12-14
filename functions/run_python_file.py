import os
import sys
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    abs_working_dir = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_path)

    try: 
        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_full_path):
            return f'Error: File "{file_path}" not found.'
        if not abs_full_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
    except Exception as e:
        return f"Error: {e}"


    cmd = [sys.executable, abs_full_path, *[str(a) for a in args]]


    
    try:
        result = subprocess.run(
        cmd,
        cwd=abs_working_dir,
        capture_output=True,
        text=True,
        timeout=30
        )
    except Exception as e:
        return f"Error: executing Python file: {e}"


    if result.returncode == 0:
        return (
            f'STDOUT:\n{result.stdout}\n'
            f'STDERR:\n{result.stderr}'
        )
    elif(result.stdout=="" and result.stderr==""):
        return "No output produced"
    else:
        return(
            f'STDOUT:\n{result.stdout}\n'
            f'STDERR:\n{result.stderr}'
            f'Process exited with code {result.returncode}'
        )