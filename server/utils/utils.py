import json
import re

@staticmethod
def load_json(response: str):
    json_matches = re.findall(r'```json(.*?)```', response, re.DOTALL)
    if json_matches:
        last_json_str = json_matches[-1]
        try:
            print(last_json_str)
            return json.loads(last_json_str)
        except json.JSONDecodeError:
            print("Error in decoding the json")
            return None
    else:
        print("No JSON found")
        return None