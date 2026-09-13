FROM python:3.12-slim-bookworm

# Create non-root user
RUN useradd --uid 1000 --create-home --shell /bin/bash appuser

WORKDIR /home/appuser/py_connector

# Install dependencies as root
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy app code directly as appuser (no chown-layer)
COPY --chown=appuser:appuser . .

# Switch to unprivileged user
USER appuser

EXPOSE 3000

# workers=1
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "3000"]
