FROM heroku/miniconda

MAINTAINER Jeremy Smith "j.smith.03@cantab.net"

# Grab requirements.txt
ADD ./app/requirements.txt /tmp/requirements.txt

# Install dependencies
RUN pip install -qr /tmp/requirements.txt

# Add our code
ADD ./app /opt/app/
WORKDIR /opt/app

# Install scientific dependencies.
RUN conda install pandas=0.20.3
RUN conda install scikit-learn=0.19.0

CMD gunicorn --bind 0.0.0.0:$PORT wsgi
