import os
from time import strftime, gmtime

def compare_date_and_size_of_two_files (file1, file2, file_log=None, compare_precision=2, abs_pathes_in_log=False):
    stat1 = os.stat(file1)
    stat2 = os.stat(file2)
    if stat1.st_size == stat2.st_size:
        if (compare_precision<0 and strftime('%Y%m%d%H%M%S',gmtime(stat1.st_mtime))==strftime('%Y%m%d%H%M%S',gmtime(stat2.st_mtime))) or \
           (compare_precision>=0 and abs(stat1.st_mtime-stat2.st_mtime)<=compare_precision):
            return True
        else:
            if file_log:
                file_log.write(
                    'Times are not equal {0}: {2} ({4}), {1}: {3} ({5}) '.format(
                        os.path.abspath(file1).decode('cp1251') if abs_pathes_in_log else os.path.split(file1)[1].decode('cp1251'),
                        os.path.abspath(file2).decode('cp1251') if abs_pathes_in_log else os.path.split(file2)[1].decode('cp1251'),
                        strftime('%Y.%m.%d %H:%M:%S',gmtime(stat1.st_mtime)),
                        strftime('%Y.%m.%d %H:%M:%S',gmtime(stat2.st_mtime)),stat1.st_mtime,stat2.st_mtime)+'\n')
            return False
    else:
        if file_log:
            file_log.write(
                'Sizes are not equal {0}: {2} bytes, {1}: {3} bytes'.format(
                    os.path.abspath(file1).decode('cp1251') if abs_pathes_in_log else os.path.split(file1)[1].decode('cp1251'),
                    os.path.abspath(file2).decode('cp1251') if abs_pathes_in_log else os.path.split(file2)[1].decode('cp1251'),
                    stat1.st_size, stat2.st_size)+'\n')
        return False

if __name__ == "__main__":
    import sys

    def getargs():
        try:
            dir1, dir2 = sys.argv[1:]
        except:
             print("Usage: gns_compare_file_sz_dt.py dir1 dir2")
             sys.exit(1)
        else:
            return (dir1, dir2)

    file1, file2 = getargs()
    log=open('log.txt','w')
    compare_date_and_size_of_two_files(file1, file2,file_log=log, abs_pathes_in_log=False,compare_precision=-1)
    log.close()