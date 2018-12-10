# Trustele

by @blockchainaire

### About Package

#### command
`pyinstaller -F --add-data venv\Lib\site-packages\chromedriver_binary\chromedriver.exe;. --icon=logo.ico --clean -w main.py`

#### about icon:
ico file need to match different sizes in Windows 7/10, if not own ico may not be loaded in every display scenario.
use this website to transfer png to ico http://icoconvert.com/

#### about Chrome driver packing
##### all in one package
two ways to pack chromedriver.exe:
1. use pyinstaller --add-binary, need to copy chrome.exe beside the main.exe
[reference](https://dotblogs.com.tw/what_s_note/2018/03/10/003044)
2. use pyinstaller --add-data, pack chromedriver.exe into the main.exe
[reference](https://codeday.me/bug/20180921/253827.html)

no need inspect getting path and add executable_path for Chrome class

use official way sys._MEIPASS
[reference](https://pyinstaller.readthedocs.io/en/v3.3.1/runtime-information.html)

it's ok copy chromedriver.exe to current path and add sys._MEIPASS to os.environ['PATH'].

##### black screen problem
modify venv/lib/site-packages/selenium/webdriver/common/services.py
add creationflags=subprocess.CREATE_NO_WINDOW argument for Popen
[reference](https://blog.csdn.net/La_vie_est_belle/article/details/81252588)
