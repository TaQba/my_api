FROM python:3.6

LABEL maintainer "Network Team <nt@names.co.uk>"
LABEL description "Nginx + uWSGI + Flask based on Alpine Linux and managed by Supervisord"

# updates and new installs
RUN apt-get update
RUN apt-get install -y --no-install-recommends apt-utils libatlas-base-dev gfortran nginx supervisor cron vim

# upgrade pip3
RUN pip3 install --upgrade pip

# Install UWSGI
RUN pip3 install uwsgi

# Copy python requirements file
COPY configs/requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

RUN useradd --no-create-home nginx

# Copy the Nginx global conf
COPY configs/nginx.conf /etc/nginx/

# Copy the Flask Nginx site conf
COPY configs/flask-site-nginx.conf /etc/nginx/conf.d/

# Copy the base uWSGI ini
COPY configs/uwsgi.ini /etc/uwsgi/

# Custom Supervisord config
COPY configs/supervisord.conf /etc/supervisord.conf

# Create app logs folder
RUN mkdir -p /code/logs
RUN chmod a+x /code/logs

ADD . /code
WORKDIR /code
RUN chmod +x bin/configure_dev_env.sh
RUN ./bin/configure_dev_env.sh

CMD ["/usr/bin/supervisord"]