from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/suchennuo/book-example.git'

# 由于域名还是裸写的 ip , 所以这一章暂且跳过
# chapter 9.1 - 9.4

def deploy():
    site_folder = '/home/%s/sites/%s' % (env.user, env.host)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_static_files(source_folder)
    _update_virtualenv(source_folder)
    _update_database(source_folder)

def _create_directory_structure_if_necessary(sit_folder):
    pass

def _get_latest_source(source_folder):
    pass

def _update_settings(source_folder, site_name):
    pass

def _update_virtualenv(source_folder):
    pass

def _update_static_files(source_folder):
    pass

def _update_database(source_folder):
    pass
