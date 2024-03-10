#!/usr/bin/env bash
# Bash script that sets up the web servers for the deployment of web_static.

server="\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}"
file="/etc/nginx/sites-available/default"

# Check if Nginx is installed and running
if ! command -v nginx >/dev/null 2>&1; then
    echo "Nginx is not installed. Installing now..."
    sudo apt update && sudo apt install -y nginx
else
    echo "Nginx is already installed and running."
fi

sudo mkdir -p "/data/web_static/releases/test/"
sudo mkdir "/data/web_static/shared/"
echo "Holberton" > "/data/web_static/releases/test/index.html"
rm -f "/data/web_static/current"; ln -s "/data/web_static/releases/test/" "/data/web_static/current"
sudo chown -hR ubuntu:ubuntu "/data/"
sudo sed -i "26i\ $server" "$file"

sudo service nginx restart
