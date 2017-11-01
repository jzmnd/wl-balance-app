FROM continuumio/miniconda

WORKDIR /app

# Grab requirements.txt.
COPY . /app
RUN pip install -r /app/requirements.txt

# Disable Intel optimizations (takes a lot of extra space).
RUN conda install nomkl

# Install scientific dependencies.
RUN conda install scikit-learn=0.19.0
RUN conda install pandas=0.20.3
RUN conda install scipy=0.19.1

# ONBUILD ADD . /app/
CMD gunicorn --bind 0.0.0.0:$PORT wsgi