# Set environment variable
echo "export PYTHONPATH=/var/hermercury" >> /var/.bashrc
source /var/.bashrc


# Install python, pip, and python modules
apt-get update
apt-get -y install python
apt-get -y install python-pip
pip install --upgrade pip

pip install feedparser


# Setup the cron
chmod +x /var/hermercury/main.py
crontab /var/hermercury/environment/hermercury_crontab