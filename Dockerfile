# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app


# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy the pyproject.toml and poetry.lock files into the container
COPY pyproject.toml ./ 

# Install the required packages using Poetry
RUN poetry install

# Copy the rest of the application code into the container
COPY . .

# Specify the command to run the application
CMD ["sh", "-c", "PYTHONPATH=/app poetry run python dialogue_dinners_signal_bot/main.py"]