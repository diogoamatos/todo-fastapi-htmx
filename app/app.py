from fastapi import FastAPI


app = FastAPI()


@app.get("/", tags=["root"])
async def root():
    return {"data": "Hello"}
