#!/usr/bin/env bash
# Bash script that sets up the web servers for the deployment of web_static.
set -e # Exit immediately if a command exits with a non-zero status.

# Check if Nginx is installed and running
if ! command -v nginx >/dev/null 2>&1; then
	echo "Nginx is not installed. Installing now..."
	sudo apt update && sudo apt install -y nginx
else
	echo "Nginx is already installed and running."
fi

# Define directories
data_dir="/data"
web_static_dir="$data_dir/web_static"
releases_dir="$web_static_dir/releases"
shared_dir="$web_static_dir/shared"
test_release_dir="$releases_dir/test"
test_index_file="$test_release_dir/index.html"
current_link="$web_static_dir/current"

# Create directories if they don't exist
sudo mkdir -p "$data_dir" "$web_static_dir" "$releases_dir" "$shared_dir" "$test_release_dir"

# Create a fake HTML file with simple content to test your Nginx configuration
sudo bash -c "cat > '$test_index_file' <<EOF
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
EOF"

# Remove existing symbolic link (if any) and create a new one
sudo rm -f "$current_link"
sudo ln -s "$test_release_dir" "$current_link"

# Give ownership to ubuntu user and group
sudo chown -R ubuntu:ubuntu "$data_dir"

# Create a dedicated Nginx configuration for hbnb_static
config_file="/etc/nginx/sites-available/hbnb_static"
sudo touch "$config_file"
# Ensure the symbolic link to sites-enabled for Nginx to read on startup
sudo ln -sf "$config_file" "/etc/nginx/sites-enabled/"

# Define configuration snippet for hbnb_static
config_content="
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;

    location /hbnb_static {
        alias $current_link/;
        index index.html index.htm;
    }
}
"

echo "$config_content" | sudo tee "$config_file"

# Remove default nginx site configuration to avoid conflict
sudo rm -f /etc/nginx/sites-enabled/default

# Restart Nginx to apply the changes
if command -v systemctl >/dev/null 2>&1; then
	sudo systemctl restart nginx
else
	sudo service nginx restart
fi

echo "Nginx server block for hbnb_static configured successfully."
