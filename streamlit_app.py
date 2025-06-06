import streamlit as st
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key = os.getenv("API_KEY"))

system_prompt = """You are a recipe generator. The user will give you ingredients that they have at home and you will come up with recipes using those ingredients. You will be replying in a json format:
                    {
                        "Food Name1": [the list of steps to make]
                        "Food Name2": [the list of steps to make]
                        "Food Name3": [the list of steps to make]
                     }
"""


with st.form("form"):
    user_prompt = st.text_input("What ingredients do you have?")
    submit = st.form_submit_button("Submit")
    if submit:
        response = client.chat.completions.create(
            model = "gpt-3.5-turbo-0125",
            response_format = {"type": "json_object"},
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        recipe = json.loads(response.choices[0].message.content)
        for food in recipe:
            st.write(food)
            for step in recipe[food]:
                st.write(step)
                st.write()