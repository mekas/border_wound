from util import *
import os


class Ioc:
    def __init__(self, ConfigParser):
        self.conf = ConfigParser

    def read_dir_content(self, dirpath):
        files = os.listdir(dirpath)
        files_f = []
        for file in files:
            filename, ext = get_filename_extension(file)
            if self.filter_file_by_extension(ext[1:]) and \
                    self.filter_file_by_name(filename):
                files_f.append((filename, ext))
        return files_f

    def filter_file_by_extension(self, ext):
        exts = self.conf['TEST']['Allowed_extension']
        ext_list = exts.split(',')
        ext_list = [e.strip() for e in ext_list]
        return True if ext in ext_list else False

    def filter_file_by_name(self, filename):
        flags = self.conf['TEST']['Flag']
        flag_list = flags.split(',')
        flag_list = [f.strip() for f in flag_list]
        pos = filename.rfind('_')
        file = filename[pos + 1:]
        return True if file not in flag_list else None
