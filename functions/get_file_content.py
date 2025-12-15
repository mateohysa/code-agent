import os
from config import MAX_FILE_CONTENT_LENGTH
from google.genai import types

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    abs_working_dir = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_path)

    try: 
        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    except Exception as e:
        return f"Error: {e}"

    try:
        if not os.path.isfile(abs_full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    except Exception as e:
        return f"Error: {e}"

    try:
        with open(abs_full_path, 'r') as f:
            file_content = f.read()
            if len(file_content) > MAX_FILE_CONTENT_LENGTH:
                file_content = file_content[:MAX_FILE_CONTENT_LENGTH]
                file_content += f'[...File "{file_path}" truncated at {MAX_FILE_CONTENT_LENGTH} characters]'
            return file_content

    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file in the working directory, truncating files longer than the configured maximum length.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description='Path to the file, relative to the working directory (e.g. "lorem.txt" or "pkg/file.py").',
            ),
        },
    ),
)

    