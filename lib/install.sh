cd ./maxent-master
./configure
make
sudo make install
cd ./python
sudo apt-get install python-dev
python setup.py build
sudo python setup.py install