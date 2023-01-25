import html
import re
import os
import urllib.parse
from fastapi import FastAPI, Query
from whatever_disentangler import whatever_disentangler as wd


app = FastAPI(description='A few tools I created for myself and made available as an HTTP API', )

# http://localhost:3000/urlunescape?url=https://uk.wikipedia.org/wiki/%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D0%B0
# http://localhost:3000/urlunescape?url=https://uk.wikipedia.org/wiki/%u0423%u043A%u0440%u0430%u0457%u043D%u0430
@app.get("/urlunescape")
# http://localhost:3000/urlunescape/https://uk.wikipedia.org/wiki/%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D0%B0
# http://localhost:3000/urlunescape/https://uk.wikipedia.org/wiki/%u0423%u043A%u0440%u0430%u0457%u043D%u0430
@app.get("/urlunescape/{url_to_unescape:path}")
# http://localhost:3000/unescapeurl?url=https://uk.wikipedia.org/wiki/%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D0%B0
# http://localhost:3000/unescapeurl?url=https://uk.wikipedia.org/wiki/%u0423%u043A%u0440%u0430%u0457%u043D%u0430
@app.get("/unescapeurl")
# http://localhost:3000/unescapeurl/https://uk.wikipedia.org/wiki/%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D0%B0
# http://localhost:3000/unescapeurl/https://uk.wikipedia.org/wiki/%u0423%u043A%u0440%u0430%u0457%u043D%u0430
@app.get("/unescapeurl/{url_to_unescape:path}")
# http://localhost:3000/url_unescape?url=https://uk.wikipedia.org/wiki/%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D0%B0
# http://localhost:3000/url_unescape?url=https://uk.wikipedia.org/wiki/%u0423%u043A%u0440%u0430%u0457%u043D%u0430
@app.get("/url_unescape")
# http://localhost:3000/url_unescape/https://uk.wikipedia.org/wiki/%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D0%B0
# http://localhost:3000/url_unescape/https://uk.wikipedia.org/wiki/%u0423%u043A%u0440%u0430%u0457%u043D%u0430
@app.get("/url_unescape/{url_to_unescape:path}")
# http://localhost:3000/unescape_url?url=https://uk.wikipedia.org/wiki/%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D0%B0
# http://localhost:3000/unescape_url?url=https://uk.wikipedia.org/wiki/%u0423%u043A%u0440%u0430%u0457%u043D%u0430
@app.get("/unescape_url")
# http://localhost:3000/unescape_url/https://uk.wikipedia.org/wiki/%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D0%B0
# http://localhost:3000/unescape_url/https://uk.wikipedia.org/wiki/%u0423%u043A%u0440%u0430%u0457%u043D%u0430
@app.get("/unescape_url/{url_to_unescape:path}")
async def unescape_url(url_to_unescape: str = Query(alias='url', title='Tiiiiitle', description='Descriiiiption descriiiiption descriiiiption')):
    if url_to_unescape:
        regex_patterns = {'html_entity': r'&#?\w+;', 'escaped': r'%[uU]([0-9A-Fa-f]{4})', 'percent_encoded': r'%([0-9A-Fa-f]{2})'}
        how_many_passes = 3
        for _ in range(how_many_passes):
            if re.search(regex_patterns['html_entity'], url_to_unescape):
                url_to_unescape = html.unescape(url_to_unescape)
            if re.search(regex_patterns['escaped'], url_to_unescape):
                url_to_unescape = re.sub(regex_patterns['escaped'], lambda m: chr(int(m.group(1), 16)), url_to_unescape)
            if re.search(regex_patterns['percent_encoded'], url_to_unescape):
                url_to_unescape = urllib.parse.unquote(url_to_unescape)
    return url_to_unescape


# http://localhost:3000/fix_legacy_encoding?str_to_fix=GocÅ‚awski&encoding_from=&encoding_to=&expected_str=Gocławski&recursivity_depth=
# http://localhost:3000/fix_legacy_encoding?str_to_fix=ÃƒÂ©chÃƒÂ©ancier&encoding_from=&encoding_to=&expected_str=échéancier&recursivity_depth=2
@app.get("/fix_legacy_encoding")
# http://localhost:3000/whatever_disentangler?str_to_fix=GocÅ‚awski&encoding_from=&encoding_to=&expected_str=Gocławski&recursivity_depth=
# http://localhost:3000/whatever_disentangler?str_to_fix=ÃƒÂ©chÃƒÂ©ancier&encoding_from=&encoding_to=&expected_str=échéancier&recursivity_depth=2
@app.get("/whatever_disentangler")
async def fix_legacy_encoding_async(
    str_to_fix: str = Query(min_length=1, title='Tiiiiitle', description='Descriiiiption descriiiiption descriiiiption'),
    encoding_from: str | None = Query(default=None, title='Tiiiiitle', description='Descriiiiption descriiiiption descriiiiption'),
    encoding_to: str | None = Query(default='utf_8', title='Tiiiiitle', description='Descriiiiption descriiiiption descriiiiption'),
    expected_str: str | None = Query(default=None, title='Tiiiiitle', description='Descriiiiption descriiiiption descriiiiption'),
    recursivity_depth: int | None | str = Query(default=1, ge=1, title='Tiiiiitle', description='Descriiiiption descriiiiption descriiiiption', coerce=lambda x: int(x) if isinstance(x, int) else 1)):

    print('Request params:',)
    qparams = [str_to_fix, encoding_from, encoding_to, expected_str, recursivity_depth]
    qparam_names = ['str_to_fix', 'encoding_from', 'encoding_to', 'expected_str', 'recursivity_depth']
    for pname, pvalue in zip(qparam_names, qparams):
        print(f'{pname.rjust(10)} = {repr(pvalue)} ({type(pvalue).__name__})')

    str_to_fix = None if str_to_fix is None or str_to_fix.strip() == '' else str_to_fix.strip()
    encoding_from = None if encoding_from is None or encoding_from.strip() == '' else encoding_from.strip()
    encoding_to = 'utf_8' if encoding_to is None or encoding_to.strip() == '' else encoding_to.strip()
    expected_str = None if expected_str is None or expected_str.strip() == '' else expected_str.strip()
    recursivity_depth = 1 if recursivity_depth is None or str(recursivity_depth).strip() == '' or recursivity_depth < 1 else recursivity_depth

    try:
        disentangler = wd.Disentangler()
        ret = disentangler.disentangle(
            str_to_fix=str_to_fix,
            encoding_from=encoding_from,
            encoding_to=encoding_to,
            expected_str=expected_str,
            recursivity_depth=recursivity_depth
        )
    except Exception as e:
        print(e)
    else:
        return list(ret)


if __name__ == "__main__":
    import uvicorn
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", required=True, help="Port number to run the server on")
    args = parser.parse_args()
    port = args.port

    uvicorn.run(app, host="127.0.0.1", port=port)