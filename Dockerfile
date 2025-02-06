# Use Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy dependencies and install
COPY app/requirements.txt .
RUN pip install -r requirements.txt

# Copy rest of the code
COPY app/ .

# Run the app
CMD ["flask", "run", "--host=0.0.0.0"]
