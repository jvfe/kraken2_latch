FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:6839-main

RUN apt-get update -y && apt-get install -y curl unzip
RUN apt-get update -y &&\
    apt-get install -y rsync

# Get miniconda
RUN curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh --output miniconda.sh
ENV CONDA_DIR /opt/conda
RUN bash miniconda.sh -b -p /opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH

# Get Mamba and Kraken2
RUN conda install mamba -n base -c conda-forge &&\
    mamba install -c bioconda -y kraken2

# Fix Kraken2 download script
RUN sed -i 's/ftp:/https:/' /opt/conda/libexec/rsync_from_ncbi.pl &&\
    sed -i 's/for subsection in est gb gss wgs/for subsection in gb wgs/' /opt/conda/libexec/download_taxonomy.sh

# Get Bracken
RUN curl -L \
    https://github.com/jenniferlu717/Bracken/archive/refs/tags/v2.8.tar.gz \
    -o bracken.tar.gz &&\
    tar -xvf bracken.tar.gz &&\
    cd Bracken-2.8 &&\
    sh install_bracken.sh


# Install MicroView
RUN python3 -m pip install microview==0.9.5

# STOP HERE:
# The following lines are needed to ensure your build environement works
# correctly with latch.
RUN python3 -m pip install --upgrade latch
COPY wf /root/wf
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
WORKDIR /root
