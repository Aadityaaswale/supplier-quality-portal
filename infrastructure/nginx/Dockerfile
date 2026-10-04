# ==============================================================================
# Production Nginx Dockerfile for Supplier Quality Review Portal
# Student: AADITYA ASWALE (23102B0044)
# ==============================================================================

FROM nginx:1.25-alpine

# Copy custom Nginx virtual host configuration
COPY infrastructure/nginx/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

STOPSIGNAL SIGQUIT

CMD ["nginx", "-g", "daemon off;"]
