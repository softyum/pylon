# docker build -t pylon-devops:v1.0 -f Dockerfile .
# ARG http_proxy=http://tinyproxy:8888
# ARG https_proxy=http://v2ray:10080
FROM python:3.12.7-slim

ARG uhome=/siri
WORKDIR $uhome/app
RUN useradd -d $uhome -s /bin/sh -u 5001 siri && chown -R siri:siri $uhome
USER siri

# import proxy to build image
ARG http_proxy
ARG https_proxy
# COPY --from=build /app/requirements.txt requirements.txt
# mirrors.cloud.aliyuncs.com
ARG pip_host='mirrors.aliyun.com' 
ARG pip_index="https://${pip_host}/pypi/simple/"
COPY --chown=siri:siri requirements.txt .
RUN pip install -r requirements.txt -i $pip_index --trusted-host $pip_host
COPY --chown=siri:siri . .
RUN ./manage makemigrations && ./manage.py migrate --noinput

CMD ["python", "manage.py", "runserver", '--noreload', '--insecure', '0.0.0.0:8080']
# python manage.py runserver --noreload --insecure 0.0.0.0:8080
# CMD python -m http.server --bind 0.0.0.0 --directory . 5000

# Collect static files.
# RUN python manage.py collectstatic --noinput --clear
# CMD set -xe; python manage.py migrate --noinput; gunicorn mysite.wsgi:application

# Runtime command that executes when "docker run" is called, it does the
# following:
#   1. Migrate the database.
#   2. Start the application server.
# WARNING:
#   Migrating database at the same time as starting the server IS NOT THE BEST
#   PRACTICE. The database should be migrated manually or using the release
#   phase facilities of your hosting platform. This is used only so the
#   Wagtail instance can be started with a simple "docker run" command.
