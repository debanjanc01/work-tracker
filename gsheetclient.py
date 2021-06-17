import os
import win32api, win32con
import gspread

def __get_master_url():
    mainconfigfile = os.path.join(os.environ["APPDATA"], 'gspread', 'main_config.properties')
    if os.path.exists(mainconfigfile):
        with open(mainconfigfile, 'r') as f:
            url = f.readline()
    else:
        win32api.MessageBox(0, 'Missing File: ' +  mainconfigfile, 'File Missing!', win32con.MB_ICONWARNING) 
        exit(-1)
    url = url.strip()
    return url
    
MASTER_URL = __get_master_url()
gclient = gspread.oauth()

