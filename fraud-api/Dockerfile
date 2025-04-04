# Use official Python base image
FROM python:3.11

# Set working directory inside container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything else
COPY . .

# Expose the port FastAPI will use
EXPOSE 8000

# Run the API
CMD ["uvicorn", "paysim_api_v3:app", "--host", "0.0.0.0", "--port", "8000"]
