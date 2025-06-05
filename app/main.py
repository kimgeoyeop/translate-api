from fastapi import FastAPI
from pydantic import BaseModel
from transformers import MarianTokenizer, MarianMTModel

app = FastAPI()

model_name = "Helsinki-NLP/opus-mt-ko-en"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

class TranslationRequest(BaseModel):
    text: str

@app.post("/translate")
async def translate_text(request: TranslationRequest):
    inputs = tokenizer(request.text, return_tensors="pt", padding=True, truncation=True)
    translated = model.generate(**inputs)
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
    return {"translated_text": translated_text}
