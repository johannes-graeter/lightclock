# TODO implement as class (lazy initialization)

import gc
import picoweb
import ure as re


app = picoweb.WebApp(__name__)

@app.route('/', methods=['GET', 'POST'])
def homepage(request, response):
    gc.collect()
    print(gc.mem_free())

    if request.method == 'POST':
        # TODO save config to json
        print(request)

    # Load config from json
    import ujson
    config = ujson.load(open("../config.json", "r"))

    print(gc.mem_free())

    # Render and return HTML page
    yield from picoweb.start_response(response)

    import utemplate.compiled
    template_loader = utemplate.compiled.Loader(None, "webapp/templates")
    template = template_loader.load("config.html")
    # render_template uses utemplate.source, which needs too much memory (see picoweb#24)
    # yield from app.render_template(response, "config.html", config)

    print(gc.mem_free())

    for s in template(config):
        yield from response.awrite(s)

    gc.collect()
    print(gc.mem_free())


@app.route(re.compile('^\/(.+\.css)$'), methods=['GET'])
def styles(request, response):
    yield from app.sendfile(response, request.url_match.group(1), 'text/css')


# TODO use gzip content encoding for speedup, if an encoded file is available (see picoweb#25)
# @app.route(re.compile('^\/(.+\.css)$'), methods=['GET'])
# def styles(request, response):
#     file_path = request.url_match.group(1)
#
#     if b"gzip" in request.headers[b"Accept-Encoding"]:
#         file_path_gzip = file_path + ".gz"
#         import os
#         if file_path_gzip in os.listdir("/"):
#             yield from app.sendfile(response, file_path_gzip, 'text/css', 'gzip')
#             return
#
#     yield from app.sendfile(response, file_path, 'text/css')

app.run(host="192.168.0.19", debug=True)