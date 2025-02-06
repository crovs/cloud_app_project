FROM python:3.10

WORKDIR /app

# Copy and install dependencies
COPY app/requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY app/ .

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
