# Use a Python base image
FROM python:3.12-slim

# Install system dependencies, including Faiss and swig
RUN apt-get update && apt-get install -y \
    build-essential \
    swig \
    libomp-dev \
    python3-dev \
    libfaiss-dev \
    && rm -rf /var/lib/apt/lists/*  # Clean up the apt cache to keep the image size smaller

# Set the working directory in the container
WORKDIR /app

# Copy the current directory content into the container
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port that the Streamlit app will run on
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py"]
