# TODO implement as class (lazy initialization)

import gc
import picoweb
import ure as re


app = picoweb.WebApp(__name__)

@app.route('/', methods=['GET', 'POST'])
def homepage(request, response):
    gc.collect()
    print(gc.mem_free())

    # Load config from json
    import ujson
    config = ujson.load(open("../config.json", "r"))

    # Save new config to json if given
    if request.method == 'POST':
        yield from request.read_form_data()

        config_changed = False
        for param in config:
            # Read configurable parameters, given per POST, that are not empty
            if 'html_type' in param and request.form.get(param['name']) and request.form[param['name']][0]:
                param['value'] = request.form[param['name']][0]
                config_changed = True

        if config_changed:
            config_file = open("config.json", "w")
            config_file.write(ujson.dumps(config))
            config_file.close()

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


# Use gzip content encoding for speedup, if an encoded file is available
@app.route(re.compile('^\/(.+\.css)$'), methods=['GET'])
def styles(request, response):
    file_path = request.url_match.group(1)

    if b"gzip" in request.headers[b"Accept-Encoding"]:
        print("client accepts gzip")
        file_path_gzip = file_path + ".gz"
        import os
        if file_path_gzip in os.listdir("webapp"):
            print("sending " + file_path_gzip)
            yield from app.sendfile(response, file_path_gzip, b"text/css", b"Content-Encoding: gzip\r\n"
                                                                           b"Cache-Control: max-age=86400\r\n")
            return

    yield from app.sendfile(response, file_path, b"text/css", b"Cache-Control: max-age=86400\r\n")

app.run(host="192.168.0.19", debug=True)