# Use a Python base image
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    swig \
    libomp-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory content into the container
COPY . /app

# Install FAISS using precompiled wheels
RUN pip install --upgrade pip
RUN pip install faiss-cpu==1.7.4  # explicitly installing faiss-cpu version from precompiled wheels

# Install other dependencies
RUN pip install -r requirements.txt

# Expose the port that the Streamlit app will run on
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py"]
