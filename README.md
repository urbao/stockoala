
# Stockoala

## Collect and Analyze Taiwan stock data CLI program<br/><br/>

![stockoala](https://github.com/urbao/stockoala/assets/87600155/778c5990-89fa-4749-954c-7f975310f0e1)

### Features
- cross-platform support(`Windows & Linux Ubuntu`)
- `Traditional Chinese` and `English` support
- collect `TWSE and TPEX` stock data weekly
- check which stock is at `reversal-point` for the past 5 weeks
- all data will only saved in `local machine` for privacy

### Pre-Requirements
- latest [Python 3.xx](https://www.python.org/downloads/) installed on local machine, and added to `$PATH`
- `pip` should also install `bs4`, `colorama` and `requests` packages
  ```bash
  pip install bs4 colorama requests
  ```

### Installation
***Linux(Ubuntu)***
1. Download the [latest release](https://github.com/urbao/stockoala/releases) based on platform
2. Extract the zip file, and put the `stockoala` directory on `Desktop`
3. Open terminal in the stockoala path, and run following command
   ```bash
   ./setup
   ```
4. Chmod to desktop file, and move it to proper location
   ```bash
   chmod +x stockoala.desktop
   mv stockoala.desktop ~/.local/share/applications
   ```
5. Refresh the database of desktop file
   ```bash
   update-desktop-database ~/.local/share/applications
   ```

***Windows***
1. Download the [latest release](https://github.com/urbao/stockoala/releases) based on platform
2. Extract the zip file, and put the `stockoala` directory on `Desktop`
3. Double-click the setup.exe file
4. Double-click the stockoala.exe file

### Related
[Taiwan Stock Exchange Official Website(TWSE)](https://www.twse.com.tw/en/)<br/>
[Taipei Exchange Official Website(TPEX)](https://www.tpex.org.tw/web/index.php?l=en-us)<br/>

### Authors
- [@urbao](https://www.github.com/urbao)

### Feedback
If you have any feedback, please reach out to us at zardforever1009@gmail.com

