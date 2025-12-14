import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info


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
    function_declarations=[schema_get_files_info],
)



response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents=messages,
    config=types.GenerateContentConfig(
    system_instruction=system_prompt,
    tools=[available_functions]
    )
)

if response.usage_metadata.prompt_token_count == None or response.usage_metadata.candidates_token_count == None:
    raise RuntimeError("API call failed(likely)")



if args.verbose:
    print("User prompt: " + args.prompt)
    print("Prompt tokens: " + str(response.usage_metadata.prompt_token_count))
    print("Response tokens: " + str(response.usage_metadata.candidates_token_count))

if len(response.function_calls) != 0:
    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")

print(response.text)





def main():
    print("")


if __name__ == "__main__":
    main()
