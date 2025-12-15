import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    abs_working_dir = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_path)

    try: 
        if not abs_full_path.startswith(abs_working_dir):
            return f"Error: Cannot list {directory} as it is outside the permitted working directory"
    except Exception as e:
        return f"Error: {e}"

    try:
        if not os.path.isdir(abs_full_path):
            return f'Error: "{directory}" is not a directory'
    except Exception as e:
        return f"Error: {e}"

        
    try:
        directory_list = os.listdir(abs_full_path)
        output_items = []
        
        for item in directory_list:
            item_full_path = os.path.join(abs_full_path, item)
            
            size = os.path.getsize(item_full_path)
            is_dir = os.path.isdir(item_full_path)
            line = f"- {item}: file_size={size} bytes, is_dir={is_dir}"
            output_items.append(line)
            
            
        result = "\n".join(output_items)
        return result
    except Exception as e:
        return f"Error: {e}"
            
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
