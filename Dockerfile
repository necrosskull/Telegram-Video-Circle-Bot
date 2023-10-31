FROM python:3.11.4-slim-bullseye AS python

# Create a project directory
WORKDIR /app

# Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the project
COPY . .

# Run the application
CMD python main.py