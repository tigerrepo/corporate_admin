server {
    listen       80;
    server_name admin.riceglobal.com;
    access_log  /var/log/nginx/admin.riceglobal.com.access.log;
    error_log   /var/log/nginx/admin.riceglobal.com.error.log;
    
    # FastCGI
    location / {
        fastcgi_pass    127.0.0.1:8020;
        fastcgi_read_timeout 300;
        fastcgi_param  PATH_INFO          $fastcgi_script_name;
        fastcgi_param  QUERY_STRING       $query_string;
        fastcgi_param  REQUEST_METHOD     $request_method;
        fastcgi_param  CONTENT_TYPE       $content_type;
        fastcgi_param  CONTENT_LENGTH     $content_length;

        fastcgi_param  REQUEST_URI        $request_uri;
        fastcgi_param  DOCUMENT_URI       $document_uri;
        fastcgi_param  DOCUMENT_ROOT      $document_root;
        fastcgi_param  SERVER_PROTOCOL    $server_protocol;

        fastcgi_param  GATEWAY_INTERFACE  CGI/1.1;
        fastcgi_param  SERVER_SOFTWARE    nginx/$nginx_version;

        fastcgi_param  REMOTE_ADDR        $remote_addr;
        fastcgi_param  REMOTE_PORT        $remote_port;
        fastcgi_param  SERVER_ADDR        $server_addr;
        fastcgi_param  SERVER_PORT        $server_port;
        fastcgi_param  SERVER_NAME        $server_name;

        fastcgi_param  HTTPS              $https if_not_empty;
        fastcgi_param  SCRIPT_FILENAME    $document_root$fastcgi_script_name;
    }

    location / {
        alias /var/www/admin.riceglobal.com/static/;
        autoindex off;
    }
}

