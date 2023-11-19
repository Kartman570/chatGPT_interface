Custom Chat-GPT API interface.<br>
Work in progress.<br>

Basic endpoints:<br>
__/chat/__ endpoint for post requests with conversation logging<br>
__/chat_dialogue/__ html template url<br>
__/docs/__ default FastAPI swagger<br>

Proxi endpoint (https://api.openai.com/v1/...):<br>
__/audio/speech/__<br>
__/audio/transcriptions/__<br>
__/audio/translations/__<br>

Installation:<br>
Paste correct openAI API key in __chatGPT.py__
```
poetry install --no-root
source .venv/bin/activate
```

Launching app:<br>
```uvicorn main:app --reload --host 0.0.0.0 --port 8000```

--__reload__ makes app reload every time you put some changes in code<br>
--__host 0.0.0.0__ gives permission to retrieve requests from outside your localhost<br>
--__port 8000__ is default FastAPI port. You can change it if you want<br>