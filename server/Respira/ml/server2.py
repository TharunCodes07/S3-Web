import uvicorn 
from fastapi  import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from server.Respira.model import (
    model,img
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


@app.post("/predict")
async def get_prediction(request:QueryRequest):
    response = model.predict(img)
    predicted_class = np.argmax(response, axis=1)[0]
    # Check if the predicted class is 0 or 1
    if predicted_class == 0:
        return False
    elif predicted_class == 1:
        return True

if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8002)
