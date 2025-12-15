import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_files import schema_write_file
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_files import write_file

FUNCTION_REGISTRY = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("API key not found in .env file")
    
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("prompt", type=str, help="User prompt")
parser.add_argument("--verbose",  action="store_true", help="Enable verbose output mode.")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]
available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file],
)

response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents=messages,
    config=types.GenerateContentConfig(
    system_instruction=system_prompt,
    tools=[available_functions]
    )
)

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    raw_args = function_call_part.args or {}

    if verbose:
        print(f"Calling function: {function_name}({raw_args})")

    # Look up function
    fn = FUNCTION_REGISTRY.get(function_name)
    if fn is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    
    kwargs = dict(raw_args)
    kwargs["working_directory"] = "./calculator"

   
    try:
        function_result = fn(**kwargs)
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Exception while calling {function_name}: {e}"},
                )
            ],
        )

    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )



if response.usage_metadata.prompt_token_count == None or response.usage_metadata.candidates_token_count == None:
    raise RuntimeError("API call failed(likely)")



if args.verbose:
    print("User prompt: " + args.prompt)
    print("Prompt tokens: " + str(response.usage_metadata.prompt_token_count))
    print("Response tokens: " + str(response.usage_metadata.candidates_token_count))

tool_responses = []

if getattr(response, "function_calls", None):
    for function_call_part in response.function_calls:
        tool_responses.append(call_function(function_call_part, verbose=args.verbose))

if tool_responses:

    for tool_msg in tool_responses:
        for part in tool_msg.parts:
            fr = getattr(part, "function_response", None)
            if fr is not None:
                resp = fr.response or {}
                if "result" in resp:
                    print(resp["result"])
    
    messages.append(response.candidates[0].content) 

   
    for tool_msg in tool_responses:
        messages.append(tool_msg)

    
    followup = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions],
        ),
    )
    print(followup.text)
else:
    print(response.text)
    messages.append(response)





def main():
    print("")


if __name__ == "__main__":
    main()
