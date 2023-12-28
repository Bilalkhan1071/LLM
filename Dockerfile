# Use the official Python image
FROM public.ecr.aws/lambda/python:3.10

WORKDIR /code
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/code"

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN yum install gcc -y

# Copy the rest of the application code into the container
COPY ./app ./app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose the port that FastAPI will run on
EXPOSE 8080

# Command to run the application
CMD [ "app.main.handler" ]
