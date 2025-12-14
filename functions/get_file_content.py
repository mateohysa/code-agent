import os
from config import MAX_FILE_CONTENT_LENGTH

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



    