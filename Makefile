deploy:
	make deploy-common
	make deploy-wifi
	make deploy-webapp
	make deploy-alarm
	ampy put main.py
	ampy put boot.py

deploy-without-modules:
	make deploy-common
	make deploy-wifi
	make deploy-webapp-static
	make deploy-webapp-templates
	ampy put main.py
	ampy put boot.py

deploy-common:
	ampy put config.json

deploy-wifi:
	ampy put connect_to_router.py

deploy-webapp:
	make deploy-webapp-static
	make deploy-webapp-templates
	ampy put webapp

deploy-webapp-static:
	ampy mkdir webapp
	find webapp_static -name "*.gz" -print0 | sed 's/webapp_static\///g' | xargs -0 -I % ampy put webapp_static/% webapp/%

deploy-webapp-templates:
	ampy mkdir webapp_templates
	find webapp_templates -name "*.py" -print0 | xargs -0 -I % ampy put % %

deploy-alarm:
	ampy put alarmclock

erase:
	ampy rm config.json
	ampy rm config_wifi.json
	ampy rm connect_to_router.py
	ampy rmdir webapp_static
	ampy rmdir webapp_templates
	ampy rmdir webapp
	ampy rmdir alarmclock
	ampy rm boot.py
	ampy rm main.py

webapp-static:
	find webapp_static -name "*.css" -print0 | xargs -0 -I % gzip -k -f --best %
	find webapp_static -name "*.js" -print0 | xargs -0 -I % gzip -k -f --best %

webapp-templates:
	sed -e "s/^[[:space:]]*//g" webapp_templates/config.html | tr -d '\n' > webapp_templates/config.html.min
	python3 ../utemplate/utemplate_util.py "rawcompile" webapp_templates/config.html.min
	mv webapp_templates/config_html_min.py webapp_templates/config_html.py
