"""
Main FastAPI server application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import connect_to_mongo, close_mongo_connection
from routes.user_routes import router as user_router
from routes.server_routes import router as server_router
from routes.scheduler_routes import router as scheduler_router
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Texium API",
    description="API for user management, server management, and job scheduling",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(user_router)
app.include_router(server_router)
app.include_router(scheduler_router)


@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    try:
        connect_to_mongo()
        print("✓ Application started successfully")
    except Exception as e:
        print(f"✗ Failed to start application: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    close_mongo_connection()


@app.get("/", tags=["health"])
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Texium API is running",
        "docs": "/docs"
    }


@app.get("/health", tags=["health"])
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Texium API"
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 5000))
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
