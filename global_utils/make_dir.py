import os
class DirectoryMaker:
    def make_dir(self,dir_address):
        if not os.path.isdir(dir_address):
            os.mkdir(dir_address)
        return dir_address