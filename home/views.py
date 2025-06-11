import uuid
from django.shortcuts import render
from groq import Groq


GROQ_API_KEY = "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"
SD_API_URL = "https://4bf4-34-19-25-241.ngrok-free.app/sdapi/v1/txt2img"

groq_client = Groq(api_key=GROQ_API_KEY)

def chatbot_view(request):
    if 'chat_history' not in request.session:
        request.session['chat_history'] = []

    chat_history = request.session['chat_history']
    response_text = ''

    if request.method == 'POST':
        user_input = request.POST.get('message', '')

        try:
            chat_completion = groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input},
                ]
            )
            response_text = chat_completion.choices[0].message.content

        except Exception:
            response_text = '🚨 Bot failed to respond.'

        chat_history.append({'sender': 'user', 'message': user_input})
        chat_history.append({'sender': 'bot', 'message': response_text})
        request.session['chat_history'] = chat_history

    return render(request, 'chat/chat.html', {'chat_history': chat_history})
