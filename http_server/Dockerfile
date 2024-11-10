# Use the official NGINX image as a base
FROM nginx:latest

# Set the working directory
WORKDIR /etc/nginx

# Copy your custom NGINX configuration
# Make sure this file contains logging setup
COPY nginx.conf /etc/nginx/nginx.conf

# Create necessary directories for logs
RUN mkdir -p /var/log/nginx

# Expose port 80 for HTTP traffic
EXPOSE 80

# Ensure that error logs are written to stdout
# Modify NGINX's default behavior for logging
RUN ln -sf /dev/stdout /var/log/nginx/access.log
RUN ln -sf /dev/stderr /var/log/nginx/error.log

# Start NGINX in the foreground (this is important for Docker containers)
CMD ["nginx", "-g", "daemon off;"]
