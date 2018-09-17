# SSL and server-side authentication for gRPC
# gRPC upstreams with NGINX >=1.13

This repository provides a simple example of using SSL and server-side authentication for gRPC using Python.

Python 2.7 and 3.6

gRPC: 1.9.1

## Certificate

Generate certificate for the server. Uses `openssl`.

```
make gen_key
```

## Install gRPC packages

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Generate gRPC stubs

```
make stubs
```

## Run server

```
make secure_server
```

## Run client

```
make secure_client
```

## Use nginx 1.13 grpc upstreams
### Create nginx configuration
```
upstream grpc-upstream-root {
    server 127.0.0.1:50051;
}
server {
    listen 1443 ssl http2;
    charset utf-8;
    server_name     example.domain.com;
    ssl_certificate         /path/to/server.crt;
    ssl_certificate_key     /path/to/server.key;

    location /grpcdata.ProdServer {
            grpc_pass grpcs://grpc-upstream-root;
            error_page 502 = /error502grpc;
    }

    location /grpcdata.StageServer {
            grpc_pass grpcs://grpc-upstream-root;
            error_page 502 = /error502grpc;
    }

    location = /error502grpc {
        internal;
        default_type application/grpc;
        add_header grpc-status 14;
        add_header grpc-message "unavailable";
        return 204;
    }
}
```
### Run client
#### edit host in secure_client_nginx.py and run make command
```
make secure_client_nginx
```

### Output results
#### server
```
$ make secure_server
python secure_server.py
Starting server secure. Listening on port 50051.
```
#### client
```
$ make secure_client_nginx
python secure_client.py
client send: hi prod! to Prod upstream
client send: hi stage! to Stage upstream
```
[Introducing gRPC Support with NGINX](https://www.nginx.com/blog/nginx-1-13-10-grpc/?utm_campaign=core&utm_medium=blog&utm_source=youtube&utm_content=grpc)
