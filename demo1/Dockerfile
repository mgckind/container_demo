# nginx:alpine is a very lightweight version of the web server nginx
FROM nginx:alpine

# We copy the index.html to the default path for nginx
ADD index.html /usr/share/nginx/html

# No need to add ENTRYPOINT or CMD since is already included in the nginx image
# https://github.com/nginxinc/docker-nginx/blob/f603bb3632ea6df0bc9da2179c18eb322c286298/mainline/alpine/Dockerfile
