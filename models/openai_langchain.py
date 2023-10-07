from langchain.chat_models import ChatOpenAI
#from langchain import openai
#from langchain.chat_models import ChatOpenAI
#from langchain import PromptTemplate
#from langchain.llms import OpenAI
#from langchain.chains import LLMChain, SimpleSequentialChain


import openai
import os

class OpenAiLC:
    def __init__(self):
        self.api_key = os.getenv('API_KEY')


    def generar_imagen(self, prompt):
        openai.api_key = self.api_key
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="256x256" #"1024x1024 / 512x512"
        )
        image_url = response['data'][0]['url']
        return image_url

    def openai_lc(self):
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            openai_api_key= self.api_key ,
            temperature=1,
            max_tokens=800,
            model_kwargs={"top_p": 0.9, "frequency_penalty": 0.4}
        )
        return self.llm
        
    def completion(texto):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=
            [
                {
                    "role" : "user", 
                    "content" : texto            
                }
            ]
        )
        return completion.choices[0].message["content"].strip()
