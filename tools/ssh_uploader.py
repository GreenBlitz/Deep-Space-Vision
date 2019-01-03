from pexpect import pxssh
from os import listdir
from os.path import isfile, join, splitext, isdir

non_copy_dirs = [".git", "ml", "garbage_code_dont_delete_btw", "venv"]

conn = None


def send_dir(path):
    linux_path = join("/mnt/c", path)
    for i in listdir(linux_path):
        if isfile(join(linux_path, i)) and splitext(join(linux_path, i))[1] == '.py':
            print("copying file " + join(linux_path, i))
            with open(join(linux_path, i), 'r') as f:
                content = f.read().replace('"', "'")
                i = '"%s"' % i
                conn.sendline("touch " + i)
                conn.sendline("echo \"" + content + "\" > " + i)

        elif isdir(join(linux_path, i)) and i not in non_copy_dirs:
            print("creating dir " + i)
            it = '"%s"' % i
            conn.sendline("mkdir " + it)
            conn.sendline("cd " + it)
            send_dir(join(path, i))
            conn.sendline("cd ..")


def main():
    global conn
    conn = pxssh.pxssh()
    if not conn.login(input("enter ip address: "), input("enter username: "), input("enter password: ")):
        print("failed to establish connection")
    else:
        print("connected successfully")
        conn.sendline("cd ~")
        conn.sendline("mkdir tmp_project")
        conn.sendline("cd tmp_project")
        path = input("enter path to project: ")
        path = path.replace("\\", '/')
        if path.startswith("C:\\") or path.startswith("C:/"):
            path = path[3:]
        send_dir(path)


if __name__ == "__main__":
    main()
