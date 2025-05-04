FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV OPENAI_API_KEY=''
ENV PYTHONPATH=/app

# Install curl and git for healthchecks and dependencies
RUN apt-get update && \
    apt-get install -y curl git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy just the pyproject.toml and poetry.lock* files first
COPY pyproject.toml poetry.lock* ./

# Install Poetry 2.1.2 which is compatible with Python 3.13
RUN pip install "poetry==2.1.2"

# Configure Poetry to not create a virtual environment
RUN poetry config virtualenvs.create false

# Copy the source code
COPY . .

# Install only the main dependencies first, then UI dependencies
RUN pip install langgraph>=0.0.20 openai>=1.0.0 python-dotenv>=1.0.0 pydantic>=2.0.0 && \
    pip install streamlit>=1.24.0 fastapi>=0.103.0 uvicorn>=0.23.0

# Expose ports for FastAPI and Streamlit
EXPOSE 8000 8501

# Set default command to run the FastAPI app
CMD ["uvicorn", "ui.api:app", "--host", "0.0.0.0", "--port", "8000"] 