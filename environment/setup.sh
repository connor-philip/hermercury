# Set environment variable
echo "export PYTHONPATH=/home/vagrant/hermercury" >> /home/vagrant/.bashrc
source /home/vagrant/.bashrc


# Install python, pip, and python modules
apt-get update
apt-get -y install python
apt-get -y install python-pip
pip install --upgrade pip

pip install feedparser


# Setup the cron
chmod +x /home/vagrant/hermercury/main.py
crontab /home/vagrant/hermercury/environment/hermercury_crontab