#!/bin/bash
set -e

# 1. Setup Docker init stub for container SysVinit
cat << 'EOF' > /etc/init.d/docker
#!/bin/sh
### BEGIN INIT INFO
# Provides:          docker
# Required-Start:    $network $local_fs
# Required-Stop:     $network $local_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Docker service stub
### END INIT INFO

case "$1" in
    start|restart|reload|force-reload|status)
        exit 0
        ;;
    stop)
        exit 0
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac
EOF
chmod +x /etc/init.d/docker

# 2. Copy backend files to app directory
mkdir -p /opt/supplier-quality-portal/backend
cp -r /backend/* /opt/supplier-quality-portal/backend/
chown -R deployer:deployer /opt/supplier-quality-portal

# 3. Start Gunicorn daemon in background for port 8000
pkill -f gunicorn || true
cd /opt/supplier-quality-portal/backend
export USE_SQLITE=True
export DEBUG=False
export SECRET_KEY='puppet-ansible-verification-key'
export ALLOWED_HOSTS='localhost,127.0.0.1'
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput --clear
nohup gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 2 > /var/log/portal-gunicorn.log 2>&1 &

sleep 2
curl -s http://127.0.0.1:8000/health/
echo ""
echo "Target node setup successfully initialized!"
