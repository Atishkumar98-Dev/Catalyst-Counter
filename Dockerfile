# Use the official Python image as a base
FROM python:3.10-slim
RUN apt-get update && apt-get install -y libpq-dev
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]



# ---------------------------Production------------------------------------#

# FROM python:3.10-slim


# WORKDIR /app


# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt


# COPY . .


# EXPOSE 8000

# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
