**WARNING** This library is still under development and intended for experimental purposes only.

## Examples (live)

* request: https://crac.ovh/urlunescape?url=https://uk.wikipedia.org/wiki/%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D0%B0
  * response: `"https://uk.wikipedia.org/wiki/Україна"`
* request: https://crac.ovh/urlunescape?url=https://uk.wikipedia.org/wiki/%u0423%u043A%u0440%u0430%u0457%u043D%u0430
  * response: `"https://uk.wikipedia.org/wiki/Україна"`
* request: https://crac.ovh/fix_legacy_encoding?str_to_fix=GocÅ‚awski&encoding_from=&encoding_to=&expected_str=Gocławski&recursivity_depth=
  * response (JSON):
```json
[
   {
      "str_to_fix":"GocÅ‚awski",
      "encoding_from":"cp1252",
      "fixed_str":"Gocławski",
      "encoding_to":"utf_8",
      "recursivity_depth":1
   },
   ⋮
]
```
* request: https://crac.ovh/fix_legacy_encoding?str_to_fix=ÃƒÂ©chÃƒÂ©ancier&encoding_from=&encoding_to=&expected_str=échéancier&recursivity_depth=2
  * response (JSON):
```json
[
   ⋮,
   {
      "str_to_fix":"ÃƒÂ©chÃƒÂ©ancier",
      "encoding_from":"cp1252",
      "fixed_str":"Ã©chÃ©ancier",
      "encoding_to":"utf_8",
      "recursivity_depth":2
   },
   {
      "str_to_fix":"Ã©chÃ©ancier",
      "encoding_from":"cp1252",
      "fixed_str":"échéancier",
      "encoding_to":"utf_8",
      "recursivity_depth":1
   },
   ⋮
]
```

## Installation & usage on a latest Ubuntu Linux server

### 1. Download and get into the directory

```sh
git clone ssh://git@github.com:22/kirisakow/api-py.git

cd api-py
```

### 2. Install and run as...

2. a. ...either as a Docker container:

```sh
docker build -f ./python3.10.dockerfile -t api-py-img .

docker run -d --name api-py -p ${PORT_NUM_AS_ENV_VAR}:80 api-py-img
```

2. b. ...or as a transient systemd service in a virtual environment:

```sh
sudo apt install python3.10-venv

python3 -m venv venv

source venv/bin/activate

python3 -m pip install -r ./requirements.txt

# simplest possible launch option, not recommended as it confers weak reliability:
python3 ./main.py --port ${PORT_NUM_AS_ENV_VAR} &

# a much better launch option, as a transient systemd service:
sudo systemd-run --uid=myuser --gid=myuser --same-dir --unit=api-py_$(date +%Y%m%d_%H%M%S)_myuser /usr/bin/python /home/myuser/api-py/main.py --port $PORT_NUM_AS_ENV_VAR
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
