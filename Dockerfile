FROM ubuntu:19.10

RUN apt-get update \
    && apt-get install -y software-properties-common \
    && apt-add-repository -y ppa:nginx/stable \
    && apt-get update \
    && apt-get install -y nginx \
    && apt-get install python3 -y \
    && apt-get install python3-pip -y \
    && apt-get install sqlite3 -y

COPY docker/entrypoint.sh /entrypoint.sh
COPY requirements.txt /requirements.txt
COPY create_db.sql /create_db.sql
RUN chmod 700 /entrypoint.sh
RUN python3 -m pip install -r /requirements.txt
COPY /docker/monkey_patched_library_file.py /usr/local/lib/python3.7/dist-packages/chess/__init__.py
RUN sqlite3 /var/www/html/sessions.db < /create_db.sql
RUN sed -i -e 's/location \/ {/location ~ {/g' /etc/nginx/sites-available/default
RUN sed -i -e 's/try_files $uri $uri\/ =404;/proxy_pass http:\/\/127.0.0.1:5000;/g' /etc/nginx/sites-available/default

RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

COPY . /var/www/html/

EXPOSE 80

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
#CMD ['/bin/bash','-c','\'python3 /var/www/html/main.py && nginx -g \'daemon off;\'\'']
