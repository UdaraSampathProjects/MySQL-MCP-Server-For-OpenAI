from fastapi import FastAPI
from api.mcp import router as mcp_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Include the routes from the api folder
app.include_router(mcp_router, prefix="/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)