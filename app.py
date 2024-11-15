from flask import Flask, render_template, request, jsonify
from groq import Groq
#from flask_cors import CORS
import os
app = Flask(__name__, template_folder='.')
#CORS(app)
#GROQ_API_URL = "https://api.groq.com/chat"

client = Groq(api_key='',)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/instructions')
def instructions():
    return render_template('instructions.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data['message']
    
    # Prepare messages for the Groq API
    messages = [
        {
            "role": "system",
            "content": "assistant summary in 30 words only if you want"
        },
        {
            "role": "user",
            "content": user_message
        }
    ]
    
    # Call the Groq API to get a response
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=1,
        max_tokens=40,
        top_p=1,
        stream=True,
        stop=None,
    )
    
    # Collect the response
    bot_response = ""
    for chunk in completion:
        bot_response += chunk.choices[0].delta.content or ""
    
    return jsonify({'response': bot_response})


@app.route('/response', methods=['POST'])
def response():
    user_input = request.form['user_input']
    user_option = request.form['user_option']
    
    # Combine user input and selected option to form the prompt
    prompt = f"{user_option}: {user_input}"
    
    # Prepare messages for the Groq API
    messages = [
        {
            "role": "system",
            "content": "assistant"
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
    
    # Call the Groq API to get a response
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    
    # Collect the response
    bot_response = ""
    for chunk in completion:
        bot_response += chunk.choices[0].delta.content or ""
    
    return render_template('response.html', user_input=user_input, bot_response=bot_response)

if __name__ == '__main__':
    app.run(debug=True)
