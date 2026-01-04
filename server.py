"""FastAPI web server for the Support Bot."""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# Global bot instance
bot = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize bot on startup."""
    global bot
    from support_bot import create_support_bot
    bot = create_support_bot()
    print("✅ Support Bot initialized")
    yield
    print("👋 Support Bot shutting down")


app = FastAPI(
    title="Support Bot API",
    description="AI-powered bot for managing WhatsApp, Email & LinkedIn",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS for web frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str
    success: bool = True


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "running",
        "service": "Support Bot API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Health check for container orchestration."""
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message to the Support Bot and get a response."""
    global bot
    
    if not bot:
        raise HTTPException(status_code=503, detail="Bot not initialized")
    
    try:
        result = await bot.run(request.message)
        return ChatResponse(response=result.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/email/send")
async def send_email_endpoint(
    to: str,
    subject: str,
    body: str,
    cc: str = None
):
    """Direct endpoint to send an email."""
    from support_bot.tools.email_tools import send_email
    result = send_email(to=to, subject=subject, body=body, cc=cc)
    return {"result": result}


@app.get("/email/unread")
async def get_unread_emails():
    """Get count of unread emails."""
    from support_bot.tools.email_tools import get_unread_count
    result = get_unread_count()
    return {"result": result}


@app.get("/email/recent")
async def get_recent_emails(count: int = 5):
    """Get recent emails."""
    from support_bot.tools.email_tools import read_emails
    result = read_emails(count=count)
    return {"result": result}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
