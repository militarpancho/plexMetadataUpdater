import os
import re
import subprocess
import time
def watch_file( dirs, pattern, check_interval=60 ):
    '''Return true if filename exists, if not keep checking once every check_interval seconds for time_limit seconds.
    time_limit defaults to 1 hour
    check_interval defaults to 1 minute
    '''

    while True:
        for dir in dirs:
            for file in os.listdir(dir):
                p = pattern.match(file)
                if p and (p.group('ext') in ['mp4', 'mkv', 'avi', 'mov']):
                    print("finding subtitles for {}".format(os.path.join(dir,file)))
                    subprocess.call(["python", "OpenSubtitlesDownload/OpenSubtitlesDownload.py", "--cli", "-i", "-a", "-l", "spa", os.path.join(dir,file)])
                    f = file.split(".")
                    new_f = "{} ({}).{}".format(" ".join(p.group('name').split(".")), p.group('year'), p.group('ext'))
                    new_srt = "{} ({}).spa.srt".format(" ".join(p.group('name').split(".")), p.group('year'))
                    os.rename(os.path.join(dir,file), os.path.join(dir, new_f))
                    if os.path.exists(os.path.join(dir, ".".join(f[:-1])+"_es.srt")):
                        os.rename(os.path.join(dir, ".".join(f[:-1])+"_es.srt"), os.path.join(dir, new_srt))
        # Wait for check interval seconds, then check again.
        time.sleep( check_interval )

if __name__ == '__main__':
    path = "/media/films"
    dirs = [f.path for f in os.scandir(path) if f.is_dir()]
    pattern = re.compile('(?P<name>.+)\.(?P<year>[0-9]+)\..*\.(?P<ext>.+$)')
    check_interval=3600*10
    watch_file( dirs, pattern, check_interval )
