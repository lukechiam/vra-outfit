# Use the official Nginx image as the base
FROM nginx:alpine

# Copy the repository's static files to Nginx's default public directory
COPY . /usr/share/nginx/html

# Expose port 80 for HTTP traffic
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
