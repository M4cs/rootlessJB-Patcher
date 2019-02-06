import os
import stat
import requests
import time
import sys
from glob import glob

LDID_PATH = os.path.realpath('/usr/local/bin/ldid2')
LDID_LINK = "https://github.com/xerub/ldid/raw/master/ldid2"
DPKG_PATH = os.path.realpath('/usr/local/bin/dpkg')
BREW_PATH = os.path.realpath('/usr/local/bin/brew')
PATCHER_DIR = os.path.realpath(os.getcwd() + '/patcher.sh')
CUR_DIR = os.path.realpath(os.getcwd())
try:
    print('checking For ldid2...')
    if os.path.exists(LDID_PATH):
        st = os.stat(LDID_PATH)
        oct_perm = oct(st.st_mode)
        if oct_perm[-3:] == 755:
            print(f'skipping permissions ldid2 set with: {oct_perm[-3:]}')
        else:
            print(f'ldid2 set with permissions: {oct_perm[-3:]}.\nshould be 755...')
            print('setting ldid2 permissions to 755...')
            os.chmod(LDID_PATH, 0o755)
            print('set permissions for ldid2...')
        print('ldid2 is installed and ready to be used...')
    else:
        print('ldid2 not found...')
        try:
            print('downloading ldid2')
            r = requests.get(LDID_LINK).content
            print(r)
            print('downloaded ldid2')
            print('installing ldid2')
            open(LDID_PATH, 'wb').write(r)
            print('giving ldid2 permissions')
            os.chmod(LDID_PATH, 0o755)
            print('finished installing ldid2')
        except Exception as e:
            print(f'Error: {e}')
            print('Exiting...')
            sys.exit(2)
    print('checking for patcher dependencies...')
    dpkg_exists = os.path.exists(DPKG_PATH)
    brew_exists = os.path.exists(BREW_PATH)
    if not dpkg_exists and not brew_exists:
        print('brew is not installed...')
        print('starting brew installer...')
        os.system(r'/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"')
        print('dpkg is not installed...')
        print('installing dpkg...')
        os.system('brew install dpkg')
    if not os.path.exists(PATCHER_DIR):
        print('downloading patcher script...')
        p = requests.get('https://raw.githubusercontent.com/jakeajames/rootlessJB3/master/patcher').text
        open(PATCHER_DIR, 'w').write(p)
        os.chmod(PATCHER_DIR, 0o755)
    print('starting patcher...')
    deb_path = input('enter deb to patch:')
    out_path = input('enter path for output:')
    query = PATCHER_DIR + " " + deb_path + " " + out_path
    os.system(query)
    files = []
    pattern = '*.dylib'
    for dir,_,_ in os.walk(CUR_DIR):
        files.extend(glob(os.path.join(dir, pattern)))
    for file in files:
        print('running ldid2 on ', file)
        os.system('ldid2 -S ' + file)
    os.remove(PATCHER_DIR)
    print('complete...')
except Exception as e:
    print("Error: Something fatal happened. Please restart the program.")
except KeyboardInterrupt:
    print("user cancellation...")
    sys.exit(2)
