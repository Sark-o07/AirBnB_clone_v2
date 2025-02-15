#!/usr/bin/env bash
# Bash script that sets up web servers for for the deployment of web_static
sudo apt-get update
sudo apt-get -y install nginx
sudo ufw allow 'Nginx HTTP'

sudo mkdir -p /data/web_static/{releases/test,shared}

echo "This is a test file" | sudo tee /data/web_static/releases/test/index.html > /dev/null

sudo ln -s -f /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
sudo sed -i '/listen 80 default_server/a \\n\tlocation /hbnb_static { \n\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

sudo service nginx restart
