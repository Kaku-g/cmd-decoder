import google.generativeai as genai
import os
import subprocess
import shlex
import json
import warnings


genai.configure(api_key=os.environ["API_KEY"])

model = genai.GenerativeModel('gemini-1.5-flash')

def load_cache():
    try:
        with open("cache.json",'r') as file:
            return json.load(file)
    except(FileNotFoundError,json.JSONDecodeError):
        return {}        

def save_cache(cache):
    with open('cache.json','w') as file:
        json.dump(cache,file)                      

command_cache=load_cache()
def decode_command(text):
    if text in command_cache:
        print_in_color("executing from cache",colors["blue"])
        return command_cache[text] 
    else:
         print_in_color("Executing using gemini model",colors["magenta"])
         response = model.generate_content(f"Convert this natural language instruction to a gitbash terminal: {text}.Give only the command wihtout using any prefix or suffix  in one line without any explanation")
         cleanResponse=response.text.strip('`')
         cleanResponse=cleanResponse.replace('`','')
         command_cache[text]=cleanResponse
         save_cache(command_cache)
         history(cleanResponse)
         return cleanResponse

   

def execute_command(cmd_command,working_directory):
    try:
        result = subprocess.run(cmd_command, capture_output=True, text=True, shell=True,cwd=working_directory)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return str(e)

def history(text):
    with open("history.txt",'a') as file:
        file.write(text+'\n')

def print_in_color(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")

colors = {
    "red": "31",
    "green": "32",
    "yellow": "33",
    "blue": "34",
    "magenta": "35",
    "cyan": "36",
    "white": "37",
}


current_directory= os.path.dirname(os.path.abspath(__file__))
def main():
    print_in_color("Natural Language to CMD Command Decoder",colors["green"])
    print_in_color("Type 'exit' to quit.",colors["red"])
    while True:
          user_input=input("> ")
          if user_input.lower()=="exit":
             break
          if user_input.lower()=="history":
            with open("history.txt",'r') as file:
                print(file.read())
            continue
          cmd_command=decode_command(user_input)
          if cmd_command:
            print_in_color(f"Executing:{cmd_command}",colors["green"])
            output=execute_command(cmd_command,current_directory)
            print(output)
          else:
            print("Sorry, I didn't understand that command.")
          
    
warnings.filterwarnings("ignore")



if __name__=="__main__":
    main()        
