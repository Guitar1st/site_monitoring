# Site monitoring
This is a simple library, that could be used as a reference for creating monitoring scripts using kafka and postgres.

##  How to use
- Make your virtualenv: `python3 -m venv env`
- Change `sites.json` to monitor your own sites
- Put your ssl certificates to `ssl` folder
- Put your postgres config to `configs/pgconfig.json`
- Install: `./env/bin/python setup.py install`
- Enable monitor: `chmod +x monitor.sh && ./monitor.sh`
- Enable store: `chmod +x store.sh && ./store.sh`

More options you can find in `./env/bin/site_monitoring --help`

## Tests
`./env/bin/pytest`
