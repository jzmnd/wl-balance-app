FROM continuumio/miniconda

# Grab requirements.txt.
COPY . /app
# RUN pip install -qr /app/requirements.txt

# Grab requirements.txt.
ADD ./app/requirements.txt /tmp/requirements.txt

# Install dependencies
RUN pip install -qr /tmp/requirements.txt

# Disable Intel optimizations (takes a lot of extra space).
RUN conda install nomkl

# Install scientific dependencies.
RUN conda install scikit-learn=0.19.0
RUN conda install pandas=0.20.3
RUN conda install scipy=0.19.1

# ONBUILD ADD . /app/
CMD gunicorn --bind 0.0.0.0:$PORT wsgi
