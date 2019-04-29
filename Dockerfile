FROM python:3

# Install node.js following instructions from
# https://nodejs.org/en/download/package-manager/
RUN apt-get update
RUN apt-get -y install curl
RUN curl -sL https://deb.nodesource.com/setup_11.x | bash -
RUN apt install nodejs

# Install node.js dependencies
RUN npm install
# Install python dependencies
COPY requirements-dev.txt /requirements-dev.txt
RUN pip install -r requirements-dev.txt

# Install git
RUN apt-get install -y git

# Clone ReadabiliPy and cd into it
RUN git clone https://github.com/alan-turing-institute/ReadabiliPy
WORKDIR "/ReadabiliPy"

# # Copy the code we want to benchmark
# COPY readablipy /readabilipy

# # Copy the latest benchmarks
# COPY tests/test_benchmarking.py tests/test_benchmarking.py

# Copy all of the files in the working directory
# COPY . /

# Run the benchmarks with Pytest
CMD pytest --benchmark-only
