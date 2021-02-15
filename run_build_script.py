import subprocess
import shutil

if __name__ == '__main__':
    script = open('build_script.bat').read()
    subprocess.run(script)

    exe_path = r"dist/rivals_code_inject.exe"
    extension_path = r"E:\Users\User\WebstormProjects\vscode_extension\rivals-lib\out"

    shutil.copy(src=exe_path, dst=extension_path)