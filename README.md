custom Chat-GPT API interface.<br>

instalation:<br>

>poetry install --no-root<br>
>source .venv/bin/activate<br>
>
>//insert correct openAI API key in __chatGPT.py__


launching app:<br>
```uvicorn main:app --reload --host 0.0.0.0 --port 8000```

--host	0.0.0.0 gives permission to retrieve requests from outside your localhost<br>
--port	8000 is default FastAPI port. can change on whatever you want<br>

