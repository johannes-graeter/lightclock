import gc
import picoweb
import ure as re
import utime as time
from alarmclock.with_config import WithConfig


class WebApp(WithConfig):
    def __init__(self, host, config, debug=True):
        # init config setter
        config_attributes = [
        ]
        super(WebApp, self).__init__(config_attributes, config)

        self.host = host
        self.debug = debug

        ROUTES = [
            ("/", self.homepage),
            (re.compile('^\/(.+\.css|.+\.js)$'), self.styles)
        ]

        self.app = picoweb.WebApp(__name__, ROUTES)

        gc.collect()
        if self.debug:
            print(gc.mem_free())

    def homepage(self, request, response):
        gc.collect()
        # print(gc.mem_free())

        if (request.method not in ['GET', 'POST']):
            return

        # Save new config to json if given
        if request.method == 'POST':
            yield from request.read_form_data()

            # update clock of controller, if utc_delay has been changed (instead of waiting for ntp update)
            if request.form.get('utc_delay') and request.form['utc_delay'][0] != '':
                if int(request.form['utc_delay'][0]) != self.config['utc_delay']['value']:
                    utc_diff = int(request.form['utc_delay'][0]) - self.config['utc_delay']['value']
                    tm = time.localtime()
                    tm_sec = time.mktime(
                        (tm[0], tm[1], tm[2], tm[3] + utc_diff, tm[4], tm[5], 0, 0))
                    tm = time.localtime(tm_sec)

                    # convert to format for rtc
                    tm = tm[0:3] + (0,) + tm[3:6] + (0,)
                    # set real time clock on controller
                    import machine
                    machine.RTC().datetime(tm)
                    print("new utc delay given, current time set to:")
                    print(time.localtime())
                    del tm_sec, tm, utc_diff

            config_changed = False
            for param_name, param_data in self.config.items():
                # Read configurable parameters, given per POST, that are not empty and differ from current config
                if 'html_type' in param_data and request.form.get(param_name) and request.form[param_name][0] \
                        and param_data['value'] != request.form[param_name][0]:
                    if param_data['html_type'] == 'number':
                        param_data['value'] = int(request.form[param_name][0])
                    else:
                        param_data['value'] = request.form[param_name][0]
                    config_changed = True

            if config_changed:
                import ujson as json

                if self.debug:
                    print("config changed, writing to config.json")
                config_file = open("config.json", "w")
                json.dump(self.config, config_file)
                config_file.close()

            del config_changed, param_name, param_data

        gc.collect()
        # print(gc.mem_free())

        # Render and return HTML page
        yield from picoweb.start_response(response)

        import utemplate.compiled
        template_loader = utemplate.compiled.Loader(None, "webapp_templates")
        template = template_loader.load("config.html")
        # render_template uses utemplate.source, which needs too much memory (see picoweb#24)
        # yield from app.render_template(response, "config.html", config)

        # print(gc.mem_free())

        self.config['current_time'] = {'value': time.localtime()}

        for s in template(self.config):
            yield from response.awrite(s)

        del template_loader, template, s
        gc.collect()
        if self.debug:
            print(gc.mem_free())

    # Use gzip content encoding for speedup, if an encoded file is available
    def styles(self, request, response):
        gc.collect()

        file_path = request.url_match.group(1)
        if file_path[-2:] == 'js':
            content_type = b"application/javascript"
        else:
            content_type = b"text/css"

        if b"gzip" in request.headers[b"Accept-Encoding"]:
            if self.debug:
                print("client accepts gzip")
            file_path_gzip = file_path + ".gz"
            import os
            if file_path_gzip in os.listdir("webapp"):
                if self.debug:
                    print("sending " + file_path_gzip)
                yield from self.app.sendfile(response, file_path_gzip, content_type, b"Content-Encoding: gzip\r\n"
                                                                                     b"Cache-Control: max-age=86400\r\n")
            del file_path_gzip
        else:
            yield from self.app.sendfile(response, file_path, content_type, b"Cache-Control: max-age=86400\r\n")

        del content_type, file_path
        gc.collect()
        if self.debug:
            print(gc.mem_free())

    def run(self):
        self.app.run(host=self.host, debug=self.debug)
