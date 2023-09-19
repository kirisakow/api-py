**WARNING** This library is still under development and intended for experimental purposes only.

## Various string-decoding tools

## Examples (live)

* problem: decode `https://uk.wikipedia.org/wiki/%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D0%B0`:
  * request: [`https://crac.ovh/urlunescape?url=`https://uk.wikipedia.org/wiki/%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D0%B0](https://crac.ovh/urlunescape?url=https://uk.wikipedia.org/wiki/%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D0%B0)
  * response: `"https://uk.wikipedia.org/wiki/Україна"`

* problem: decode `https://uk.wikipedia.org/wiki/%u0423%u043A%u0440%u0430%u0457%u043D%u0430`:
  * request: [`https://crac.ovh/urlunescape?url=`https://uk.wikipedia.org/wiki/%u0423%u043A%u0440%u0430%u0457%u043D%u0430](https://crac.ovh/urlunescape?url=https://uk.wikipedia.org/wiki/%u0423%u043A%u0440%u0430%u0457%u043D%u0430)
  * response: `"https://uk.wikipedia.org/wiki/Україна"`

* problem: you have a garbled string (`GocÅ‚awski`) and its fixed shape (`Gocławski`), and you need to know the source and target character encodings:
  * request: [`https://crac.ovh/fix_legacy_encoding?str_to_fix=`GocÅ‚awski`&expected_str=`Gocławski`&recursivity_depth=`](https://crac.ovh/fix_legacy_encoding?str_to_fix=GocÅ‚awski&expected_str=Gocławski&recursivity_depth=)
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

* problem: you need to perform a 2-depth recursive disentangling on a wickedly garbled string (`ÃƒÂ©chÃƒÂ©ancier`) of which you know the fixed shape (`échéancier`), and you need to know the source and target character encodings:
  * request: [`https://crac.ovh/fix_legacy_encoding?str_to_fix=`ÃƒÂ©chÃƒÂ©ancier`&expected_str=`échéancier`&recursivity_depth=`2](https://crac.ovh/fix_legacy_encoding?str_to_fix=ÃƒÂ©chÃƒÂ©ancier&expected_str=échéancier&recursivity_depth=2)
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
* problem: you need to decode a Morse string in every possible alphabet `••• −•− •− −−•• •− −• −• −−− •  •• ••• −−−• • −−•• •− • − •−•−•−  −• •− •−−• •• ••• •− −• −• −−− •  −−− ••• − •− • − ••• •−•−`:
  * requests:
    * [`https://crac.ovh/decode_morse?str_to_decode=`•••%20−•−%20•−%20−−••%20•−%20−•%20−•%20−−−%20•%20%20••%20•••%20−−−•%20•%20−−••%20•−%20•%20−%20•−•−•−%20%20−•%20•−%20•−−•%20••%20•••%20•−%20−•%20−•%20−−−%20•%20%20−−−%20•••%20−%20•−%20•%20−%20•••%20•−•−](https://crac.ovh/decode_morse?str_to_decode=•••%20−•−%20•−%20−−••%20•−%20−•%20−•%20−−−%20•%20%20••%20•••%20−−−•%20•%20−−••%20•−%20•%20−%20•−•−•−%20%20−•%20•−%20•−−•%20••%20•••%20•−%20−•%20−•%20−−−%20•%20%20−−−%20•••%20−%20•−%20•%20−%20•••%20•−•−)
    * [`https://crac.ovh/decode_morse/`•••%20−•−%20•−%20−−••%20•−%20−•%20−•%20−−−%20•%20%20••%20•••%20−−−•%20•%20−−••%20•−%20•%20−%20•−•−•−%20%20−•%20•−%20•−−•%20••%20•••%20•−%20−•%20−•%20−−−%20•%20%20−−−%20•••%20−%20•−%20•%20−%20•••%20•−•−](https://crac.ovh/decode_morse/•••%20−•−%20•−%20−−••%20•−%20−•%20−•%20−−−%20•%20%20••%20•••%20−−−•%20•%20−−••%20•−%20•%20−%20•−•−•−%20%20−•%20•−%20•−−•%20••%20•••%20•−%20−•%20−•%20−−−%20•%20%20−−−%20•••%20−%20•−%20•%20−%20•••%20•−•−)
* return as response (JSON):
```json
{
  "str_to_decode":"••• −•− •− −−•• •− −• −• −−− •  •• ••• −−−• • −−•• •− • − •−•−•−  −• •− •−−• •• ••• •− −• −• −−− •  −−− ••• − •− • − ••• •−•−",
  "cyrillic":"СКАЗАННОЕ ИСЧЕЗАЕТ, НАПИСАННОЕ ОСТАЕТСЯ",
  "latin":"SKAZANNOE ISÖEZAET, NAPISANNOE OSTAETSÄ"
}
```

* problem: you need to encode to Morse a string:
  * requests:
    * [`https://crac.ovh/encode_to_morse?str_to_encode=`СКАЗАННОЕ%20ИСЧЕЗАЕТ,%20НАПИСАННОЕ%20ОСТАЕТСЯ](https://crac.ovh/encode_to_morse?str_to_encode=СКАЗАННОЕ%20ИСЧЕЗАЕТ,%20НАПИСАННОЕ%20ОСТАЕТСЯ)
    * [`https://crac.ovh/encode_to_morse/`СКАЗАННОЕ%20ИСЧЕЗАЕТ,%20НАПИСАННОЕ%20ОСТАЕТСЯ](https://crac.ovh/encode_to_morse/СКАЗАННОЕ%20ИСЧЕЗАЕТ,%20НАПИСАННОЕ%20ОСТАЕТСЯ)
* return as response (JSON):
```json
{
  "str_to_encode": "СКАЗАННОЕ ИСЧЕЗАЕТ, НАПИСАННОЕ ОСТАЕТСЯ",
  "morse": "... -.- .- --.. .- -. -. --- .  .. ... ---. . --.. .- . - .-.-.-  -. .- .--. .. ... .- -. -. --- .  --- ... - .- . - ... .-.-"
}
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
