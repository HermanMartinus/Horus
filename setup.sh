chmod +x horus.py
cp horus.py horus
mkdir -p ~/.pwd
mv horus ~/.pwd/
cp authenticator.json ~/.pwd/
export PATH=$PATH":$HOME/.pwd"
