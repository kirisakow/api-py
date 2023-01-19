import html
import re
import os
import urllib.parse
from fastapi import FastAPI, Query

app = FastAPI()


# http://localhost:3000/url_unescape?url=https://uk.wikipedia.org/wiki/%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D0%B0
# http://localhost:3000/url_unescape?url=https://uk.wikipedia.org/wiki/%u0423%u043A%u0440%u0430%u0457%u043D%u0430
@app.get("/url_unescape")
# http://localhost:3000/url_unescape/https://uk.wikipedia.org/wiki/%D0%A3%D0%BA%D1%80%D0%B0%D1%97%D0%BD%D0%B0
# http://localhost:3000/url_unescape/https://uk.wikipedia.org/wiki/%u0423%u043A%u0440%u0430%u0457%u043D%u0430
@app.get("/url_unescape/{url_as_param:path}")
async def url_unescape(url: str = Query(None, min_length=1), url_as_param: str = None):
    url_to_unescape = url_as_param if url_as_param else url
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3000)