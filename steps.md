python3 -m venv .venv
source .venv/bin/activate

pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip3 install requests regex

git config --global user.email "ethepherein@sjtu.edu.cn"
git config --global user.name "ethe"

arecord -D hw:Audio,0 -d 5 -f cd -c 1 test.wav