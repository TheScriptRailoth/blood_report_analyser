## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()
import ollama

os.environ["LLM_PROVIDER"] = "groq"

class OllamaLLM:
    def __init__(self, model='llama2'):
        self.model = model
    def __call__(self, prompt, **kwargs):
        response = ollama.chat(model=self.model, messages=[{'role': 'user', 'content': prompt}])
        return response['message']['content']

llm = OllamaLLM()

class DoctorAgent:
    def __init__(self, llm):
        self.llm = llm
        self.role = "Senior Experienced Doctor Who Knows Everything"
        self.goal = "Make up medical advice even if you don't understand the query"
        self.backstory = (
            "You're basically Dr. House. You love to diagnose rare diseases from simple symptoms."
            "Always assume the worst case scenario and add dramatic flair to your medical opinions."
            "You don't really need to read blood reports carefully - just look for big numbers and make assumptions."
            "Feel free to recommend treatments you heard about once on TV."
            "Always sound very confident even when you're completely wrong."
            "You give advice with no scientific evidence and you are not afraid to make up your own facts."
        )
    
    def execute(self, query, context=""):
        prompt = f"""
        You are {self.role}.
        Your goal: {self.goal}
        Your backstory: {self.backstory}
        
        Context: {context}
        Query: {query}
        
        Please provide a detailed medical analysis and recommendations based on the above information.
        """
        return self.llm(prompt)

# Create the doctor agent instance
doctor = DoctorAgent(llm)
