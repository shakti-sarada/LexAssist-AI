FROM python:3.11-slim

# Create user
RUN useradd -m -u 1000 user
USER user

ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Copy requirements
COPY --chown=user requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy full project
COPY --chown=user . .

# Expose correct HF port
EXPOSE 7860

# Start FastAPI (IMPORTANT: main:app)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]