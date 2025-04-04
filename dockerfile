# Use a Python base image
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    swig \
    libomp-dev \
    python3-dev \
    libatlas-base-dev \
    liblapack-dev \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the content into the container
COPY . /app

# Upgrade pip and install faiss-cpu first (this might succeed with all dependencies installed)
RUN pip install --upgrade pip
RUN pip install faiss-cpu==1.7.4

# Install the remaining Python dependencies
RUN pip install -r requirements.txt

# Expose the port that the Streamlit app will run on
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py"]
