from gns_compare_file_sz_dt import compare_date_and_size_of_two_files
import os
from shutil import copy2, copytree, rmtree

def difference(seq1, seq2):
    return [item for item in seq1 if item not in seq2]

class DirectoriesSynchronizer (object):

    def __init__(self, dir_source, dir_target, deleting_in_target=False, log_file_name='sync_dir_log.txt'):
        if os.path.isdir(dir_source):
            self.dir_source = os.path.abspath(dir_source)
        else:
            raise ValueError, "{0} isn't correct directory name !".format (dir_source)
        if os.path.isdir(dir_target):
            self.dir_target = os.path.abspath(dir_target)
        else:
            raise ValueError, "{0} isn't correct directory name !".format (dir_target)
        self.len_source = len(self.dir_source)
        self.len_target = len(self.dir_target)
        self.walk_source = os.walk(self.dir_source)
        self.walk_target_dict = {}
        for base_trg, dirs_trg, files_trg in os.walk(self.dir_target):
            self.walk_target_dict [base_trg[self.len_target:]] = files_trg
        self.log_file_name = log_file_name
        self.deleting_in_target = deleting_in_target

    def sync_files (self, base_src, files_src, base_trg, files_trg):
        for f in [item for item in files_src if item in files_trg]:
            fsrc = os.path.join(base_src,f)
            if not compare_date_and_size_of_two_files(fsrc, os.path.join(base_trg,f), file_log=self.file_log, end_log_string=''):
                copy2 (fsrc, base_trg)
                self.file_log.write (' Copied.\n')
        for f in difference(files_src, files_trg):
            self.file_log.write("Copying absent file {2} from {1} to {0}.".format(base_trg, base_src, f))
            copy2 (os.path.join(base_src,f), base_trg)
            self.file_log.write(" Ok."+'\n')
        for f in difference(files_trg, files_src):
            self.file_log.write('File {} is absent in directory {}.'.format(f, base_src))
            if self.deleting_in_target:
                os.remove(os.path.join(base_trg,f))
                self.file_log.write (' Deleted.\n')
            else:
                self.file_log.write ('\n')

    def run_synchronization (self):
        self.file_log = open(self.log_file_name,'w')
        for base_src, dirs_src, files_src in self.walk_source:
            base_trg = base_src.replace(self.dir_source,self.dir_target)
            if base_src[self.len_source:] in self.walk_target_dict:
                files_trg = self.walk_target_dict.pop(base_src[self.len_source:])
                self.sync_files(base_src, files_src, base_trg, files_trg)
            elif not os.path.exists(base_trg):
                self.file_log.write(
                   'Copying absent subdirectory {2} from {1} to {0}.'.format(os.path.split(base_trg)[0],
                                                                            *os.path.split(base_src)))
                copytree(base_src, base_trg)
                self.file_log.write(' Ok.\n')
        for dir in self.walk_target_dict:
            splt = os.path.split(os.path.join(self.dir_target,dir[1:]))
            if not splt[0][self.len_target:] in self.walk_target_dict:
                self.file_log.write('Subdirectory {} is absent in directory {}.'.format(splt[1],splt[0].replace(self.dir_target, self.dir_source)))
                if self.deleting_in_target:
                    rmtree(os.path.join(splt[0],splt[1]))
                    self.file_log.write (' Deleted.\n')
                else:
                    self.file_log.write ('\n')
        self.file_log.close()

if __name__ == "__main__":
    import sys

    def getargs():
        if len (sys.argv) > 3:
            dir1, dir2 = sys.argv[1:3]
            delete_flag = sys.argv[3].upper() == '/D'
        elif len (sys.argv) == 3:
            delete_flag = False
            dir1, dir2 = sys.argv[1:]
        else:
             print("Usage: sync_dirs.py dir1 dir2 [/d]")
             sys.exit(1)

        return (dir1, dir2, delete_flag)

    dir1, dir2, delete_flag = getargs()
    DirectoriesSynchronizer (dir1, dir2, deleting_in_target=delete_flag).run_synchronization()
