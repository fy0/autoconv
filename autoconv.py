"""
{
    "global": {
        "encoder": "opusenc.exe",
        "input_dir": "input",
        "output_dir": "output",
        "watch_ext": [".wav"],
        "output_ext": ".opus"
    },
    "types": {
        "music": {
            "--title": "track title"
        }
    }
}

"""

import os
import json
import time
from pathlib import Path  # py3.4+
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

config = {}


def convert(type_name, filepath):    
    if len(filepath.parts) == 1:
        return
    if filepath.suffix not in config['global']['watch_ext']:
        return

    if type_name in config['types']:
        typeinfo = config['types'][type_name]
        
        params = []
        for k, v in typeinfo.items():
            params.append('%s %s' % (k, v))

        out_path = Path(config['global']['output_dir']).joinpath(filepath)
        out_ext = config['global']['output_ext']

        cmd = [
            config['global']['encoder'],
            ' '.join(params),
            str(Path(config['global']['input_dir']).joinpath(filepath)),
            str(out_path)[:-len(out_path.suffix)] + out_ext  # .absolute()
        ]

        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        cmd = ' '.join(cmd)
        print('Running: %s' % cmd)
        os.system(cmd)
    return True


class FileEventHandler(FileSystemEventHandler):
    def on_moved(self, event):
        if event.is_directory:
            print("directory moved from {0} to {1}".format(event.src_path,event.dest_path))
        else:
            path = Path(event.dest_path).relative_to(config['global']['input_dir'])
            if convert(path.parts[0], path):
                print("file moved from {0} to {1}".format(event.src_path,event.dest_path))

    def on_modified(self, event):
        if not event.is_directory:
            path = Path(event.src_path).relative_to(config['global']['input_dir'])
            if convert(path.parts[0], path):
                print("file modified: %s" % event.src_path)



def main():
    global config
    config = json.loads(open('config.json', encoding='utf-8').read())
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler, config['global']['input_dir'], True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    main()
