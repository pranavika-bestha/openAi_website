import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import AzureOpenAI
from dotenv import load_dotenv

# OpenTelemetry imports
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# ---- LOAD ENV VARIABLES ----
load_dotenv()  # load .env file

AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")  # from .env
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://jon-m900oi9e-eastus2.cognitiveservices.azure.com/")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION", "2025-01-01-preview")

# ---- INITIALIZE AZURE OPENAI CLIENT ----
client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    api_version=AZURE_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)

# ---- INITIALIZE OPENTELEMETRY ----
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
span_processor = BatchSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)

# ---- FASTAPI SETUP ----
app = FastAPI()
FastAPIInstrumentor.instrument_app(app)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- REQUEST MODEL ----
class ChatRequest(BaseModel):
    message: str

# ---- CHAT ENDPOINT WITH TRACING ----
@app.post("/chat")
async def chat(request: ChatRequest):
    with tracer.start_as_current_span("process_chat_message"):
        # Send user message to Azure OpenAI
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[{"role": "user", "content": request.message}]
        )
        reply_content = response.choices[0].message.content
        return {"reply": reply_content}
