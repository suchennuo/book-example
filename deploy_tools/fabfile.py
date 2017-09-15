from fabric.contrib.files import append, exists, sed, is_link
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/suchennuo/book-example.git'

APP_NAME = 'superlists'
env.user = 'chao'

def deploy():
    # /home/chao/sites/superlists
    site_folder = f'/home/{env.user}/sites/{APP_NAME}'
    # /home/chao/sites/superlists/source
    source_folder = site_folder + '/source'

    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)

    _nginx_config(source_folder)
    _nginx_create_symlink()
    _gunicorn_config(source_folder)


def _create_directory_structure_if_necessary(sit_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run(f'mkdir -p {sit_folder}/{subfolder}')

def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')


def _update_settings(source_folder, site_name):
    setting_path = source_folder + '/superlists/settings.py'
    sed(setting_path, "DEBUG = True", "DEBUG = False")
    sed(setting_path,
        'ALLOWED_HOSTS = .+$',
        f'ALLOWED_HOSTS = ["{site_name}"]'
    )

    '''
    Django 用 SECRET_KEY 来做一些加密——比如 cookies 和 CSRF. 最佳实践是保持 server 上的
    secret key 与 源码里的不同。
    '''
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}" ')
    append(setting_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder):
    # /home/chao/sites/superlists/source/../virtualenv
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip3'):
        run(f'python3 -m venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip3 install -r {source_folder}/requirements.txt')


def _update_static_files(source_folder):
    run(
        f'cd {source_folder} && ../virtualenv/bin/python3 manage.py collectstatic --noinput')

def _update_database(source_folder):
    run(
        f'cd {source_folder} && ../virtualenv/bin/python3 manage.py migrate --noinput'
    )

def _nginx_config(source_floder):
    run(
        f'cat {source_floder}/deploy_tools/nginx.template.conf  | sudo tee /etc/nginx/sites-available/superlists'
    )
def _nginx_create_symlink():
    if not exists('/etc/nginx/sites-enabled/superlists'):
        run(
            'sudo ln -s /etc/nginx/sites-available/superlists /etc/nginx/sites-enabled/superlists'
        )

def _gunicorn_config(source_floder):
    run(
        f'cat {source_floder}/deploy_tools/gunicorn-systemd.template.service | sudo tee /etc/systemd/system/gunicorn-superlists.service'
    )
    run('sudo systemctl daemon-reload')
    run('/etc/init.d/nginx start')
    run('sudo systemctl enable gunicorn-superlists.service')
    run('sudo systemctl start gunicorn-superlists.service')