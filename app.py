from flask import Flask, render_template, request
import openai

app = Flask(__name__)

openai.api_key = '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'

message_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    input_text = request.form['input_text']

    if input_text.lower() == 'new chat':
        message_history.clear()  # clear previous chat history
        return render_template('index.html')

    message_history.append({"role": "user", "content": f"{input_text}"})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_history
    )

    reply_content = completion.choices[0].message.content

    message_history.append({"role": "assistant", "content": f"{reply_content}"})

    response = [(message_history[i]["content"], message_history[i+1]["content"]) for i in range(0, len(message_history)-1, 2)]

    return render_template('index.html', response=response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
