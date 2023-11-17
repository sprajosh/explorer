from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import List
from utils.chat_processor import ChatProcessor
import tempfile
import json

app = FastAPI()

@app.post("/")
async def process_files(questions: UploadFile = File(...), file: UploadFile = File(...)):
    try:
        questions = json.loads(await questions.read())

        file_ext = '.' + file.filename.split('.')[-1]
        with tempfile.NamedTemporaryFile(delete=False, mode='wb', suffix=file_ext) as temp_file:
            file_content = await file.read()
            temp_file.write(file_content)
            temp_file_path = temp_file.name

        chat_processor = ChatProcessor(api_key='sk-', file_path=temp_file_path)

        results = chat_processor.process_chat(questions)
        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
