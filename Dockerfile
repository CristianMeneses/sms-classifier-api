FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# CPU-only torch to keep the image size under control (~700MB vs ~2.5GB with CUDA)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 7860

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
