import os
from google.genai import types

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    abs_working_dir = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_path)

    try: 
        if not abs_full_path.startswith(abs_working_dir):
            return f"Error: Cannot list {file_path} as it is outside the permitted working directory"
    except Exception as e:
        return f"Error: {e}"

    try: 
        with open(abs_full_path, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes text content to a file within the working directory, creating or overwriting the file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description='Path to the file to write, relative to the working directory (e.g. "output.txt" or "pkg/data.txt").',
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write into the file.",
            ),
        },
    ),
)