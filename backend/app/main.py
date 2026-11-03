from fastapi import FastAPI

app = FastAPI(
    title="PJ Platform API",
    description="API para intermediação de serviços PJ",
    version="1.0.0"
)

@app.get("/")
def root():
    return { "message" : "API is running"}

@app.get("/status")
def root():
    return { "status" : "healthy"}