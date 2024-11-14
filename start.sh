# sh start.sh
set -e
cwd=$(realpath $(dirname $0))
echo "deploy_work_dir = $cwd"

alias pyruntime=./fp1289/.venv/bin/python/
pyruntime $cwd/manage.py runserver 127.0.0.1:8080
# --noreload --insecure

cat <<'//comments'

Test by `curl -H 'Cookie: uidpylon=xxx'`
curl --no-buffer 127.0.0.1:8080

//comments

<<'//comments'
# /etc/systemd/system/pylon.service
[Unit]
Description=pyops Service
After=network.target nss-lookup.target

[Service]
User=root
WorkingDirectory=/app/pyops
ExecStart=/app/.venv/bin/python manage.py runserver 127.0.0.1:8080 --noreload --insecure
#Environment=DOCKER_CONTEXT=pod01.dev
Restart=on-failure
MemoryMax=256M

[Install]
WantedBy=multi-user.target
//comments

<<'//comments'
# * * * * * flock -n /var/lock/cron_debug.lock -c "sh /my_job.sh 2>&1 | tee -a /tmp/cron_debug.log"
# The -n option tells flock not to wait indefinitely. 
# If it can't acquire the lock, it will exit immediately. 
# If you want it to wait until the lock is available, you can remove the -n option.
flock -n /var/lock/cron_debug.lock -c "sh -ec 'date ; sleep 300; date' 2>&1 | tee -a /tmp/cron_debug.log"
//comments
