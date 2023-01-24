## Installation & usage on a latest Ubuntu Linux server

### 1. Download and get into the directory

```sh
git clone ssh://git@github.com:22/kirisakow/api-py.git

cd api-py
```

### 2. Install and run as...

2. a. ...as a Docker container:

```sh
docker build -f ./python3.10.dockerfile -t api-py-img

docker run -d --name api-py -p ${PORT_NUM_AS_ENV_VAR}:80 api-py-img
```

2. b. ...in a venv:

```sh
sudo apt install python3.10-venv

python3 -m venv venv

source venv/bin/activate

python3 -m pip install -r ./requirements.txt

python3 ./main.py --port ${PORT_NUM_AS_ENV_VAR} &
```

3. Configure Nginx as reverse proxy, for example:

```sh
server {
   server_name ${DOMAIN_NAME_AS_ENV_VAR};

   location ~ ^/(endpoint|another_endpoint|yet_another) {
       proxy_pass http://localhost:${PORT_NUM_AS_ENV_VAR};
   }

   #
   # ...TLS / SSL / HTTPS / LetsEncrypt / certbot stuff...
   #

}
server {
   #
   # ...TLS / SSL / HTTPS / LetsEncrypt / certbot stuff...
   #
}
```

4. Test Nginx configuration and, if valid, restart Nginx service:

```sh
sudo nginx -t && sudo systemctl restart nginx.service
```
