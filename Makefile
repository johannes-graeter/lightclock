deploy:
	make deploy-common
	make deploy-wifi
	make deploy-webapp
	make deploy-alarm
	ampy put boot.py
	ampy put main.py

deploy-without-modules:
	make deploy-common
	make deploy-wifi
	make deploy-webapp-static
	make deploy-webapp-templates
	ampy put boot.py
	ampy put main.py

deploy-common:
	ampy put config.json

deploy-wifi:
	ampy put config_wifi.json
	ampy put connect_to_router.py

deploy-webapp:
	make deploy-webapp-static
	make deploy-webapp-templates
	ampy put webapp

deploy-webapp-static:
	ampy put webapp_static

deploy-webapp-templates:
	ampy put webapp_templates

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
