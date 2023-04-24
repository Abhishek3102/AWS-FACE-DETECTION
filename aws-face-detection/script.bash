sudo apt update -y
sudo apt upgrade -y
sudo apt install python3-pip -y
sudo pip3 install -r requirements.txt
sudo pip3 install "uvicorn[standard]"
sudo pip3 install pillow
sudo uvicorn main:app --host 0.0.0.0 