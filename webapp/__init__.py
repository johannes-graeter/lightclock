import gc
import picoweb
import ure as re


class WebApp():

    def __init__(self):
        ROUTES = [
            ("/", self.homepage),
            (re.compile('^\/(.+\.css|.+\.js)$'), self.styles)
        ]

        self.app = picoweb.WebApp(__name__, ROUTES)

        gc.collect()
        print(gc.mem_free())

    def homepage(self, request, response):
        gc.collect()
        print(gc.mem_free())

        if (request.method not in ['GET', 'POST']):
            return

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

            del config_changed, param

        gc.collect()
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

        del config, template_loader, template, s
        gc.collect()
        print(gc.mem_free())


    def styles(self, request, response):
        if (request.method not in ['GET']):
            return

        yield from self.app.sendfile(response, request.url_match.group(1))

        gc.collect()
        print(gc.mem_free())


    # TODO use gzip content encoding for speedup, if an encoded file is available (see picoweb#25)
    # def styles(request, response):
    #     file_path = request.url_match.group(1)
    #
    #     if b"gzip" in request.headers[b"Accept-Encoding"]:
    #         file_path_gzip = file_path + ".gz"
    #         import os
    #         if file_path_gzip in os.listdir("/"):
    #             yield from self.app.sendfile(response, file_path_gzip, 'text/css', 'gzip')
    #             return
    #
    #     yield from self.app.sendfile(response, file_path, 'text/css')

    def run(self):
        self.app.run(host="192.168.0.27", debug=True)
        #self.app.run(host="192.168.4.1", debug=True) # AP_IF