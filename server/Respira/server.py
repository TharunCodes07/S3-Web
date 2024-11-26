import uvicorn 
from fastapi  import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from model import (
    load_and_preprocess_image, model
)

import os

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    print('Loading')
    

@app.post("/prediction")
async def get_response(request:QueryRequest):
    img_array = load_and_preprocess_image(r"D:\Coding\React\Project UI\LearnScope\VerdictIQ\public\upload.jpeg")
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)[0]
    if predicted_class == 1:
        return {"response": "Pneumonia Positive"}
    else:
        return {"response": "Pneumonia Negative"}




# @app.post("/predict")
# async def get_prediction(request:QueryRequest):
#     response = model.predict(img)
#     predicted_class = np.argmax(response, axis=1)[0]
#     # Check if the predicted class is 0 or 1
#     if predicted_class == 0:
#         return False
#     elif predicted_class == 1:
#         return True

if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8006)
