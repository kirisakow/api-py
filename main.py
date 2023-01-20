import html
import re
import os
import urllib.parse
from fastapi import FastAPI, Query

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
async def fix_legacy_encoding_async(
    str_to_fix: str = Query(min_length=1, title='Tiiiiitle', description='Descriiiiption descriiiiption descriiiiption'),
    encoding_from: str | None = Query(default=None, title='Tiiiiitle', description='Descriiiiption descriiiiption descriiiiption'),
    encoding_to: str | None = Query(default='utf_8', title='Tiiiiitle', description='Descriiiiption descriiiiption descriiiiption'),
    expected_str: str | None = Query(default=None, title='Tiiiiitle', description='Descriiiiption descriiiiption descriiiiption'),
    recursivity_depth: int | None | str = Query(default=1, ge=1, title='Tiiiiitle', description='Descriiiiption descriiiiption descriiiiption', coerce=lambda x: int(x) if isinstance(x, int) else 1)):

    def fix_legacy_encoding(*, str_to_fix: str, encoding_from=None, encoding_to=None, expected_str=None, recursivity_depth=1):
        if str_to_fix is None or str_to_fix.strip() == '':
            raise ValueError(f"The required parameter str_to_fix (string to fix) is empty.")

        def _fix(str_to_fix: str, encoding_from: str, encoding_to: str):
            return str_to_fix.encode(encoding_from).decode(encoding_to, errors='replace')

        def _resolve_encodings(enc):
            if isinstance(enc, str):
                return [enc]
            if isinstance(enc, list):
                return enc
            elif enc is None:
                # Copied from https://docs.python.org/3/library/codecs.html#standard-encodings
                with open('standard_encodings.txt', 'r') as f:
                    standard_encodings = f.read().splitlines()
                return standard_encodings

        cache = []
        def _fix_legacy_encoding(str_to_fix: str, _encoding_from: list, _encoding_to: list, expected_str: str, recursivity_depth: int):
            for enc_from in _encoding_from:
                for enc_to in _encoding_to:
                    if enc_from == enc_to:
                        continue
                    try:
                        fixed_str = _fix(str_to_fix, enc_from, enc_to)
                    except UnicodeEncodeError:
                        pass
                    except Exception as e:
                        print(e)
                    else:
                        return_pack = {
                            "str_to_fix": str_to_fix,
                            "encoding_from": enc_from,
                            "fixed_str": fixed_str,
                            "encoding_to": enc_to,
                            "recursivity_depth": recursivity_depth
                        }
                        if (expected_str is None
                        or expected_str.strip() == ''
                        or expected_str.strip().lower() == fixed_str.strip().lower()
                        or recursivity_depth > 1):
                            if return_pack not in cache:
                                cache.append(return_pack)
                                yield return_pack
                        if recursivity_depth > 1:
                            decremented_depth = recursivity_depth - 1
                            yield from _fix_legacy_encoding(fixed_str, _encoding_from, _encoding_to, expected_str, decremented_depth)

        yield from _fix_legacy_encoding(str_to_fix, _resolve_encodings(encoding_from), _resolve_encodings(encoding_to), expected_str, recursivity_depth)

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
        ret = fix_legacy_encoding(
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
    uvicorn.run(app, host="127.0.0.1", port=3000)