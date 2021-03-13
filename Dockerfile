# Import the FastApi Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

# Sets up a directory for the application in the container
WORKDIR /usr/src/app

# Copy all the source code to the container
COPY . ./

# Install dependencies needed as specified in the requirements.txt file
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# set up redis
RUN wget https://download.redis.io/releases/redis-6.0.10.tar.gz && tar xzf redis-6.0.10.tar.gz && cd redis-6.0.10 && make && src/redis-server --daemonize yes

# Run the application with python
CMD ["python", "-m", "src.Tr4PrFnPredApp.app"]