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
    
@staticmethod
def filter_results(results: list):
    filtered_results = []
    for result in results:
        num_fields = len(result)
        empty_fields = 0
        for _, value in result.items():
            if value is None:
                empty_fields += 1
            elif str(value) == "" or str(value) == "N/A" or str(value) == "0" or str(value) == "-":
                empty_fields += 1

        if empty_fields > (2*num_fields / 3):
            continue
        
        filtered_results.append(result)
        
    return filtered_results