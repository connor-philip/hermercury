# Set environment variable
echo "export PYTHONPATH=/home/vagrant/hermercury" >> /home/vagrant/.bashrc
source /home/vagrant/.bashrc


#Install python, pip, and python modules
apt-get update
apt-get -y install python
apt-get -y install python-pip
pip install --upgrade pip

pip install feedparser
