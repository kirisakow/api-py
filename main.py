from fastapi import FastAPI, Query
import html
import logging
import os
import re
import subprocess
import sys
import urllib.parse

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), '../whatever_disentangler'
        )
    )
)
from whatever_disentangler import Disentangler

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), '../telegram_bots'
        )
    )
)
from utils import JournalLogger

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), '../morse_decoder_encoder'
        )
    )
)
from morse_decoder_encoder import decode_from_morse, encode_to_ansi_morse


logging.basicConfig(level=logging.DEBUG)
jl = JournalLogger(program_name='api-py')

app = FastAPI(
    description='A few tools I created for myself and made available as an HTTP API', )


# http://localhost:3000/urlunescape?url=https://uk.wikipedia.org/wiki/%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D0%B0
# http://localhost:3000/urlunescape?url=https://uk.wikipedia.org/wiki/%u0423%u043A%u0440%u0430%u0457%u043D%u0430
@app.get("/urlunescape")
# http://localhost:3000/urlunescape/https://uk.wikipedia.org/wiki/%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D0%B0
# http://localhost:3000/urlunescape/https://uk.wikipedia.org/wiki/%u0423%u043A%u0440%u0430%u0457%u043D%u0430
@app.get("/urlunescape/{url:path}")
# http://localhost:3000/unescapeurl?url=https://uk.wikipedia.org/wiki/%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D0%B0
# http://localhost:3000/unescapeurl?url=https://uk.wikipedia.org/wiki/%u0423%u043A%u0440%u0430%u0457%u043D%u0430
@app.get("/unescapeurl")
# http://localhost:3000/unescapeurl/https://uk.wikipedia.org/wiki/%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D0%B0
# http://localhost:3000/unescapeurl/https://uk.wikipedia.org/wiki/%u0423%u043A%u0440%u0430%u0457%u043D%u0430
@app.get("/unescapeurl/{url:path}")
# http://localhost:3000/url_unescape?url=https://uk.wikipedia.org/wiki/%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D0%B0
# http://localhost:3000/url_unescape?url=https://uk.wikipedia.org/wiki/%u0423%u043A%u0440%u0430%u0457%u043D%u0430
@app.get("/url_unescape")
# http://localhost:3000/url_unescape/https://uk.wikipedia.org/wiki/%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D0%B0
# http://localhost:3000/url_unescape/https://uk.wikipedia.org/wiki/%u0423%u043A%u0440%u0430%u0457%u043D%u0430
@app.get("/url_unescape/{url:path}")
# http://localhost:3000/unescape_url?url=https://uk.wikipedia.org/wiki/%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D0%B0
# http://localhost:3000/unescape_url?url=https://uk.wikipedia.org/wiki/%u0423%u043A%u0440%u0430%u0457%u043D%u0430
@app.get("/unescape_url")
# http://localhost:3000/unescape_url/https://uk.wikipedia.org/wiki/%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D0%B0
# http://localhost:3000/unescape_url/https://uk.wikipedia.org/wiki/%u0423%u043A%u0440%u0430%u0457%u043D%u0430
@app.get("/unescape_url/{url:path}")
async def unescape_url(url: str) -> str:
    url_to_unescape = url
    jl.print(f"url_to_unescape: {url_to_unescape}")
    proc_url_unescape = subprocess.Popen(
        ['/usr/bin/python', '../url_tools/url_unescape.py', url_to_unescape],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    output_as_bytes, err_as_bytes = proc_url_unescape.communicate()
    if err_as_bytes and not output_as_bytes:
        jl.print(err_as_bytes)
    return output_as_bytes.decode().strip('\n')


# http://localhost:3000/fix_legacy_encoding?str_to_fix=GocÅ‚awski&encoding_from=&encoding_to=&expected_str=Gocławski&recursivity_depth=
# http://localhost:3000/fix_legacy_encoding?str_to_fix=ÃƒÂ©chÃƒÂ©ancier&encoding_from=&encoding_to=&expected_str=échéancier&recursivity_depth=2
@app.get("/fix_legacy_encoding")
# http://localhost:3000/whatever_disentangler?str_to_fix=GocÅ‚awski&encoding_from=&encoding_to=&expected_str=Gocławski&recursivity_depth=
# http://localhost:3000/whatever_disentangler?str_to_fix=ÃƒÂ©chÃƒÂ©ancier&encoding_from=&encoding_to=&expected_str=échéancier&recursivity_depth=2
@app.get("/whatever_disentangler")
async def fix_legacy_encoding_async(
        str_to_fix: str = Query(min_length=1, title='Tiiiiitle',
                                description='Descriiiiption descriiiiption descriiiiption'),
        encoding_from: str | None = Query(
            default=None, title='Tiiiiitle', description='Descriiiiption descriiiiption descriiiiption'),
        encoding_to: str | None = Query(
            default='utf_8', title='Tiiiiitle', description='Descriiiiption descriiiiption descriiiiption'),
        expected_str: str | None = Query(
            default=None, title='Tiiiiitle', description='Descriiiiption descriiiiption descriiiiption'),
        recursivity_depth: int | None | str = Query(default=1, ge=1, title='Tiiiiitle', description='Descriiiiption descriiiiption descriiiiption', coerce=lambda x: int(x) if isinstance(x, int) else 1)):

    jl.print('Request params:',)
    qparams = [str_to_fix, encoding_from,
               encoding_to, expected_str, recursivity_depth]
    qparam_names = ['str_to_fix', 'encoding_from',
                    'encoding_to', 'expected_str', 'recursivity_depth']
    for pname, pvalue in zip(qparam_names, qparams):
        jl.print(f'{pname.rjust(10)} = {repr(pvalue)} ({type(pvalue).__name__})')

    def emptyOrNone(v):
        return v is None or str(v) == ''

    str_to_fix = None if emptyOrNone(str_to_fix) else str_to_fix.strip()
    encoding_from = None if emptyOrNone(
        encoding_from) else encoding_from.strip()
    encoding_to = 'utf_8' if emptyOrNone(encoding_to) else encoding_to.strip()
    expected_str = None if emptyOrNone(expected_str) else expected_str.strip()
    recursivity_depth = 1 if emptyOrNone(recursivity_depth) \
        or int(recursivity_depth) < 1 \
        else int(recursivity_depth)

    try:
        disentangler = Disentangler()
        ret = disentangler.disentangle(
            str_to_fix=str_to_fix,
            encoding_from=encoding_from,
            encoding_to=encoding_to,
            expected_str=expected_str,
            recursivity_depth=recursivity_depth
        )
    except Exception as e:
        jl.print(e)
    else:
        return list(ret)


# http://localhost:3000/decode_morse?str_to_decode=•••%20−•−%20•−%20−−••%20•−%20−•%20−•%20−−−%20•%20%20••%20•••%20−−−•%20•%20−−••%20•−%20•%20−%20•−•−•−%20%20−•%20•−%20•−−•%20••%20•••%20•−%20−•%20−•%20−−−%20•%20%20−−−%20•••%20−%20•−%20•%20−%20•••%20•−•−
@app.get("/decode_morse")
# http://localhost:3000/decode_morse/•••%20−•−%20•−%20−−••%20•−%20−•%20−•%20−−−%20•%20%20••%20•••%20−−−•%20•%20−−••%20•−%20•%20−%20•−•−•−%20%20−•%20•−%20•−−•%20••%20•••%20•−%20−•%20−•%20−−−%20•%20%20−−−%20•••%20−%20•−%20•%20−%20•••%20•−•−
@app.get("/decode_morse/{str_to_decode}")
async def decode_morse(str_to_decode: str) -> dict:
    jl.print(f'{str_to_decode = }')
    return decode_from_morse(str_to_decode)

# http://localhost:3000/encode_to_morse?str_to_encode=СКАЗАННОЕ%20ИСЧЕЗАЕТ,%20НАПИСАННОЕ%20ОСТАЕТСЯ
@app.get("/encode_to_morse")
# http://localhost:3000/encode_to_morse/СКАЗАННОЕ%20ИСЧЕЗАЕТ,%20НАПИСАННОЕ%20ОСТАЕТСЯ
@app.get("/encode_to_morse/{str_to_encode}")
async def encode_to_morse(str_to_encode: str) -> dict:
    jl.print(f'{str_to_encode = }')
    return encode_to_ansi_morse(str_to_encode)


if __name__ == "__main__":
    import uvicorn
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", required=True,
                        help="Port number to run the server on")
    args = parser.parse_args()
    port = int(args.port)

    uvicorn.run(app, host="127.0.0.1", port=port)
