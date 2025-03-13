# -*- coding: utf-8 -*-

import os, sys, json
from flask import Flask, request, flash, url_for, \
    redirect, render_template, session, jsonify
import google.generativeai as genai

app = Flask(__name__)
app.config['SECRET_KEY'] = 'adambaylin'

genai.configure(api_key='')

# List available models
print("Available models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"- {m.name}")

model = genai.GenerativeModel('models/gemini-1.5-flash')

@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        prompt_type = request.form['prompt_type']
        input_text = request.form['input_text']
        
        if prompt_type == 'rewrite':
            prompt = f"Trả lời bằng tiếng Việt: Viết lại đoạn văn sau: {input_text}"
        elif prompt_type == 'outline':
            prompt = f"Trả lời bằng tiếng Việt: Tạo outline cho đoạn văn sau: {input_text}"
        elif prompt_type == 'detail':
            prompt = f"Trả lời bằng tiếng Việt: Mở rộng outline sau thành chi tiết: {input_text}"
        else:
            prompt = f"Trả lời bằng tiếng Việt: {input_text}"  # Default to just using the input text as prompt and ask for Vietnamese response

        try:
            response = model.generate_content(prompt)
            output_text = response.text
        except Exception as e:
            output_text = f"Error generating response: {e}"

        return render_template('home.html', output_text=output_text, input_text=input_text)

    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
