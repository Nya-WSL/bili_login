import os
import time
import shutil

from version import version
from pathlib import Path

main_py = "main.py"
app_name = "bili_login"

os.makedirs(Path("dist", app_name), exist_ok=True)

start_time = time.time()

os.system(f"uv run nuitka --onefile --windows-icon-from-ico=logo.ico {main_py} --include-package=nicegui --include-package-data=nicegui --windows-console-mode=disable --product-name={app_name} --product-version={version} --copyright=Nya-WSL --output-dir=dist --output-filename={app_name}.exe")

end_time = time.time()

print(f"Nuitka编译完成，耗时{end_time - start_time:.2f}秒")

shutil.copy(Path("dist", f"{app_name}.exe"), Path("dist", app_name, f"{app_name}.exe"))