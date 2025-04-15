from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import the API router
from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title="Finance API",
    description="Finance App API for stocks, market indices, and more",
    version="0.1.0",
)

# Set CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins, adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API router with a prefix
app.include_router(api_router, prefix=settings.API_V1_STR)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Finance API. Go to /docs for documentation."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8006) 