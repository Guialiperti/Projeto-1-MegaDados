from fastapi import FastAPI
import uvicorn

app=FastAPI()

@app.get("/read_data")
def test_root():
    return{"Hello":"world"}