FROM python:3.10-slim # No user function so will run at Root

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy required files for security (also configure .dockerignore for extra security)

# ONLY USE COPY . . FOR DEBUGGING IF NEEDED
# COPY . . 
COPY app/ ./app/
COPY wsgi.py .
# COPY scripts/init-db-script.py ./scripts

EXPOSE 5000

# Command to run the app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]