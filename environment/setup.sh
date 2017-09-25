PROJECTDIR=/var/hermercury

# Set environment variable
echo "export PYTHONPATH=$PROJECTDIR" >> /var/.bashrc
source /var/.bashrc


# Create config from config_template if config.py does not already exist
ls $PROJECTDIR | grep config.py || cp $PROJECTDIR/config_template.py $PROJECTDIR/config.py


# Install python, pip, and python modules
apt-get update
apt-get -y install python
apt-get -y install python-pip
pip install --upgrade pip

pip install feedparser


# Setup the cron
chmod +x $PROJECTDIR/main.py
crontab $PROJECTDIR/environment/hermercury_crontab