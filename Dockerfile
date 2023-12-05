# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Install uWSGI
RUN pip install uwsgi

# Copy project
COPY . /code/

# uWSGI will listen on this port
EXPOSE 8000

# uWSGI configuration (adjust accordingly)
CMD ["uwsgi", "--socket", ":8000", "--module", "Syncmore.wsgi", "--processes", "4", "--threads", "2"]
