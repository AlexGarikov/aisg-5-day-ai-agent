import google.generativeai as genai
import ast
import re
from utils import AiTools

class AI_Agent():
    def __init__(self, gemini_api_key):
        genai.configure(api_key=gemini_api_key)
        #for m in genai.list_models():
        #    print(m)
        self.model = genai.GenerativeModel("gemini-2.0-flash-exp")
        self.ai_toolbox = AiTools()

        # Map available functions
        self.available_functions = {
            "getLocation": self.ai_toolbox.getLocation,
            "getCurrentWeather": self.ai_toolbox.getCurrentWeather,
            "list_events": self.ai_toolbox.cal_service.list_events,
            "create_event": self.ai_toolbox.cal_service.create_event,
            "delete_event": self.ai_toolbox.cal_service.delete_event,
            "shift_event": self.ai_toolbox.cal_service.shift_event,
            "get_current_datetime": self.ai_toolbox.get_current_datetime
        }

    def do_action(self, query, max_calls=5):
        # Combine the system prompt and user query into a single input because gemini does not take messages arrays like GPT!
        full_prompt = f"{self.ai_toolbox.prompt}\nUser: {query}\nAssistant: "
        action_regex = r"^Action: (\w+): (.*)$"
        # call the llm atleast 3 times

        result_msg = []
        for i in range(max_calls):
            result_msg.append(f"Call {i + 1}:")

            response = self.model.generate_content(full_prompt)
            # print(response.parts[0].text)
            response_text = response.text
            result_msg.append(response_text)
            full_prompt += response_text

            # Split response text into lines
            response_lines = response.text.strip().split("\n")

            # Find the action string in the response
            found_action_str = next((line for line in response_lines if re.match(action_regex, line)), None)

            # Execute the identified action if it matches
            actions = re.match(action_regex, found_action_str) if found_action_str else None
            if actions:
                action, action_arg = actions.groups()
                if action in self.available_functions:
                    # print(f'args: {action_arg}')
                    necessary_func = self.available_functions[action]
                    # print(f'func: {necessary_func}')
                    try:
                        action_arg = ast.literal_eval(action_arg)
                    except:
                        pass
                    if not isinstance(action_arg, tuple):
                        action_arg = (action_arg,)
                    observation = necessary_func(*action_arg)
                    # print(f'observation: {observation}')
                    full_prompt = full_prompt + f'\nObservation: {observation}\n'
                else:
                    result_msg.append(f"Action '{action}' is not available.")
            else:
                #result_msg.append("Done")
                break

        result = '\n'.join(result_msg)
        return result