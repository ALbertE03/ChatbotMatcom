import streamlit as st
import requests
import os
import json
import numpy as np
from embedder import Embedder

os.environ["STREAMLIT_SECRETS_PATH"] = ".streamlit/secrets.toml"


class Chat:
    def __init__(self, model, api_key=None):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        self.model = model
        self.url = "https://api.fireworks.ai/inference/v1/chat/completions"
        self.e = Embedder(
            "MarkdownFile.md",
            chunk_size=10000,
            output_dir="output",
            output_prefix="chunk",
        )

    def run(self, input, history):
        with open("prompts.json", encoding="utf-8") as f:
            data = json.load(f)

        k = 3
        context = ""
        top_indices, top_scores, top_file_names = self.e.query_top_k(input, k=k)
        for idx, score, fname in zip(top_indices, top_scores, top_file_names):
            context += self.e.file_contents(fname)
        param = {
            "history": history,
            "context": context.replace("\n", ""),
            "input": input,
        }
        prompt_template = data["formacion_formacional"]["prompt"].format(**param)
        print(prompt_template)
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": f"{prompt_template}",
                    "name": "User",
                }
            ],
        }

        response = requests.request(
            "POST", self.url, json=payload, headers=self.headers
        )
        return json.loads(response.text)
