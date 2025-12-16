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
from config import MAX_STEPS
from call_function import call_function



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

for step in range (MAX_STEPS):
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=messages,
        config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        tools=[available_functions]
        ),
    )

    function_calls = getattr(response, "function_calls", None)

    if function_calls:
        tool_responses = []
        for function_call_part in function_calls:
            tool_msg = call_function(function_call_part, verbose=args.verbose)
            tool_responses.append(tool_msg)
        
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
        continue
    print(response.text)
    break


if response.usage_metadata.prompt_token_count == None or response.usage_metadata.candidates_token_count == None:
    raise RuntimeError("API call failed(likely)")

if args.verbose:
    print("User prompt: " + args.prompt)
    print("Prompt tokens: " + str(response.usage_metadata.prompt_token_count))
    print("Response tokens: " + str(response.usage_metadata.candidates_token_count))

def main():
    print("")


if __name__ == "__main__":
    main()
