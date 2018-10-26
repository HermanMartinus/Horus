chmod +x horus.py
cp horus.py horus
mkdir -p ~/bin
mv horus ~/bin/
cp authenticator.json ~/bin/
export PATH=$PATH":$HOME/bin"
