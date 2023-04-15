from typing import Dict, List
from Agents.Func.initialize_agent import set_model_api
from Agents.Func.initialize_agent import language_model_api
from Utilities.storage_interface import StorageInterface


class ExecutionAgent:
    generate_text = None
    storage = None

    def __init__(self):
        # Add your initialization code here
        self.generate_text = set_model_api()
        self.storage = StorageInterface()

    def run_execution_agent(self, objective: str, params: Dict) -> str:
        #print(self.storage.get_storage().get())
        try:
            context = [task['task_desc'] for task in self.storage.get_storage().get()]
        except:
            context = []
        print(f"\nContext: {context}")
        task = ["Develop a task list"]
        if language_model_api == 'openai_api':
            prompt = [
                {"role": "system",
                 "content": f"You are an AI who performs one task based on the following objective: {objective}.\n"},
                {"role": "user",
                 "content": f"Take into account these previously completed tasks: {context}\nYour task: {task}\nResponse:"},
            ]
        else:
            print('\nLanguage Model Not Found!')
            raise ValueError('Language model not found. Please check the language_model_api variable.')

        result = self.generate_text(prompt, params).strip()

        print(f"\n\nExec: {result}")
        # quit()

        try:
            self.storage.save_results(task, result)
        except Exception as e:
            print("Error during upsert:", e)

        # print(self.storage.get_result(task))

        return result