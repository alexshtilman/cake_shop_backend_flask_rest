FROM python:3.6

# Expose ports
EXPOSE 5000

# Tell Python to not generate .pyc
ENV PYTHONDONTWRITEBYTECODE 1

# Install requirements using pip
ADD requirements.txt .
RUN python -m pip install -r requirements.txt

# Set working directory and addour Flask API files
WORKDIR /app
ADD . /app