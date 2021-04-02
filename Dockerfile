# Import the FastApi Dockerfile
FROM continuumio/miniconda3

# Sets up a directory for the application in the container
WORKDIR /usr/src/app

# Copy all the source code to the container
COPY . ./
RUN conda env create -f environment.yml

# Install protein function predictions library
RUN /opt/conda/envs/Tr4PrFnPredApp/bin/pip install --upgrade pip && /opt/conda/envs/Tr4PrFnPredApp/bin/pip install --no-dependencies git+git://github.com/Tr4PrFnPred/Tr4PrFnPredLib.git && /opt/conda/envs/Tr4PrFnPredApp/bin/pip install python-multipart && /opt/conda/envs/Tr4PrFnPredApp/bin/pip install torch && /opt/conda/envs/Tr4PrFnPredApp/bin/pip install redis && /opt/conda/envs/Tr4PrFnPredApp/bin/pip install Jinja2

# set up redis
RUN apt-get update && apt-get install -y build-essential && wget https://download.redis.io/releases/redis-6.0.10.tar.gz && tar xzf redis-6.0.10.tar.gz && cd redis-6.0.10 && make && src/redis-server --daemonize yes

# Run the application with python
ENTRYPOINT ["conda", "run", "-n", "Tr4PrFnPredApp", "python", "-m", "src.Tr4PrFnPredApp.app"]
