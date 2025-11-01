# Use nginx alpine for lightweight image
FROM nginx:alpine

# Copy all static files to nginx html directory
COPY index.html /usr/share/nginx/html/
COPY style.css /usr/share/nginx/html/
COPY app.js /usr/share/nginx/html/
COPY *.json /usr/share/nginx/html/

# Copy question data files (txt and pdf) for reference
COPY *.txt /usr/share/nginx/html/
COPY *.pdf /usr/share/nginx/html/

# Copy Python scripts (optional - for regenerating questions)
COPY *.py /usr/share/nginx/html/

# Copy README and LICENSE
COPY README.md /usr/share/nginx/html/
COPY LICENSE /usr/share/nginx/html/
COPY CLAUDE.md /usr/share/nginx/html/

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
