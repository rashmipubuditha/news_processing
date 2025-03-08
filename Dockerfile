FROM continuumio/miniconda3:latest

# Set the working directory
WORKDIR /app

# Install OpenJDK (Java)
RUN apt-get update && apt-get install -y openjdk-17-jdk

# Set the correct JAVA_HOME path
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Verify Java installation
RUN java -version

# Create and activate the Conda environment
RUN conda create -n newsenv python=3.11.5 && \
    conda install -n newsenv -y -c conda-forge \
    pyspark pytorch numpy pandas scipy scikit-learn orjson pyarrow s3fs \
    umap-learn onnxruntime spacy transformers gensim numba sqlalchemy pytest &&\
    conda clean --all -y

# Set the environment variable to activate the Conda environment by default
ENV PATH="/opt/conda/envs/newsenv/bin:$PATH"

# Copy project files
COPY src /app/src
COPY config /app/config
COPY dataset /app/dataset
COPY scripts /app/scripts

# Run script
ENTRYPOINT ["/bin/bash", "/app/scripts/run.sh"]
