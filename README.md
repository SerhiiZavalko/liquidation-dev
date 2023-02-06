# Odoo project template
## Install dependencies
sudo add-apt-repository ppa:linuxuprising/libpng12 &&
sudo apt update &&
sudo apt install git python3-pip build-essential wget python3-dev python3-venv python3-wheel libxslt-dev libzip-dev libldap2-dev libsasl2-dev python3-setuptools libjpeg-dev libpng12-0 gdebi gcc libpq-dev -y
sudo apt-get install nodejs npm -y
sudo npm install -g rtlcss

## Configure postgresql
sudo -u postgres createuser --superuser $(whoami)
<!-- psql --dbname template1 -c "alter role $(whoami) with password 'newpassword'" -->

## Configure git
git config --global user.name "SerhiiZavalko"
git config --global user.email sergey.zavalko@gmail.com

## Configure dev environment
### 20.0.4
python3 -m venv env
source env/bin/activate
mkdir src local bin filestore logs
git clone -b 14.0 --single-branch --depth 1 https://github.com/odoo/odoo.git src/odoo
env/bin/pip install setuptools wheel debugpy scrypt && env/bin/pip install -r src/odoo/requirements.txt

env/bin/pip install paramiko py3o.template py3o.formats


## Get config
src/odoo/odoo-bin --config odoo.conf --addons-path src/odoo/odoo/addons,src/odoo/addons,addons-default,addons-dev --data-dir filestore --save --stop-after-init

## Run server
bin/odoo





## Misc commands
### modules
python3 -c 'help("modules")'

### debug attach
python3 -m debugpy --listen 5678 src/odoo/odoo-bin -c odoo.conf
### ports
sudo ss -ltnp

### Ubuntu
xdg-open http://localhost:8069/web
chmod +x bin/odoo

ln -s ~/projects/learn/odoo/book/Odoo_14_Development_Cookbook.pdf ~/Desktop/OdooCookbook.pdf


### Odoo
src/odoo/odoo-bin scaffold scaffolded_module local-dev/
odoo-bin scaffold -h
odoo-bin scaffold -t path/to/template my_module
By default, Odoo has two templates in the /odoo/cli/templates directory. One is the default template, and the second is the theme template.

### error
Warn: Can't find .pfb for face 'Times-Roman'

git clone -b 15.0 --single-branch --depth 1 https://github.com/OCA/web.git odoo-web/15.0





self.partner_id.bank_account_count
bin/odoo -u l10n_ua_classifier --limit-time-real=100000
