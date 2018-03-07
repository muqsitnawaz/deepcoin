sudo apt-get install python3-pip python3-dev python-virtualenv
virtualenv --system-site-packages -p python3 ~/tensorflow
source ~/tensorflow/bin/activate
easy_install -U pip
pip3 install --upgrade tensorflow
source ~/tensorflow/bin/activate
deactivate
sudo -H pip3 install tensorflow
sudo -H pip3 install keras
sudo -H pip3 install pillow
sudo -H pip3 install h5py
