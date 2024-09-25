# Official Python runtime as a parent image
FROM python:3.9-slim

WORKDIR /app

#Copy the necessary files
RUN mkdir -p /app/utils
COPY utils /app/utils
COPY app.py /app/
COPY requirements.txt /app/


# Set the environment variable
ARG MY_SECRET_KEY
ENV OPENAI_API_KEY=${MY_SECRET_KEY}
ENV NAME=CHATPDF

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run app.py when the container launches
CMD ["streamlit", "run", "app.py"]
