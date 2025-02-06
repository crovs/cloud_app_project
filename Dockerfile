FROM python:3.10

WORKDIR /app


ENV FLASK_APP=app:create_app
ENV FLASK_RUN_HOST=0.0.0.0

# Upgrade pip and install dependencies with no cache
COPY app/requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY app/ .

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]

