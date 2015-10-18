server {
        server_name cdn.riceglobal.com;
        access_log /var/log/nginx/cdn.riceglobal.com.access.log;
        error_log  /var/log/nginx/cdn.riceglobal.com.error.log;

        location /gallery {
            alias /var/www/cdn.riceglobal.com/gallery;
        }
        location /video {
            alias /var/www/cdn.riceglobal.com/video;
        }
}
