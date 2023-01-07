
# Stockoala

Combine functionality of Collect/Analyze Taiwan stock data together running via terminal<br/><br/>



![Logo](https://cdn-icons-png.flaticon.com/256/424/424783.png)


## Features

- collect **TWSE and TPEX** stock data by user specific period **(Max/min Price)**
- check which stock is at **Reverse Point** for the most recent date
- push all data and result to GitHub **(Backup Purpose)**
- view contents of data file with **user-defined column counts**

## Run Locally

Clone the project

```bash
  git clone git@github.com:urbao/stockoala.git
```

Go to the project directory

```bash
  cd "DIRECTORY_PATH"
```

Make file executable

```bash
  chmod +x install.sh
```

Start install process

```bash
  ./install.sh
```


## Appendix

- Make sure **git init** and **add your repo as origin** is done before using stockoala<br/>
- **Default value  of 'install.sh'** can be modified based on personal preference<br/>
- For examples, **dirpath** can be changed from **"$HOME/Desktop/stockoala"** to **"$HOME/Documents/stockoala"** depends on you<br/>
- And, **dsktpath, iconpath** and **usrname** can also be done just like this<br/>
- **HOWEVER, make sure the path is valid!!!**
## Screenshots

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)


## Related

Here are some related stock market official link

[Taiwan Stock Exchange](https://www.twse.com.tw/zh/page/trading/exchange/STOCK_DAY.html)<br/>
[Taipei Exchange](https://www.tpex.org.tw/web/stock/aftertrading/daily_trading_info/st43.php?l=zh-tw)<br/>

## FAQ

#### Question 1: What's the structure of whole project?<br/>

Ans: Use Python and Bash to collect given period **Taipei Exchange and Taiwan Stock Exchange data**, and the **Python** does the most job of **collecting and parsing**, while **Bash** controls the **workflow and the fileviewer task**<br/>
#### Question 2: Can this project run on Windows?<br/>

Ans: Maybe, It depends on condition of your PC.<br/> If **Windows Subsystem for Linux and Python3** is installed, it might works. The *ONLY* thing that is for sure is **Running on Ubuntu 22.04 works really well**<br/> 

## Authors

- [@urbao](https://www.github.com/urbao)


## Feedback

If you have any feedback, please reach out to us at zardforever1009@gmail.com

