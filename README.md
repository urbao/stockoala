
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

Remove original .git/ dir

```bash
rm -rf .git/
```
New your own repositary in GitHub<br/>
Start your own git
```bash
git init
git add ./
git commit -m "First commit"
```

Replace YOUR_REPO_URL with your own url
```bash
git remote add origin "YOUR_REPO_URL"
```

Push the dir to GitHub
```bash
git push -u origin master
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

- **Default value  of 'install.sh'** can be modified based on personal preference<br/>
- For examples, **dirpath** can be changed from **"$HOME/Desktop/stockoala"** to **"$HOME/Documents/stockoala"** depends on you<br/>
- And, **dsktpath, iconpath** and **usrname** can also be done just like this<br/>
- **HOWEVER, make sure the path is valid!!!**
## Screenshots

1. Installation<br/>![Installation](https://user-images.githubusercontent.com/87600155/211139578-d6650af4-8c76-46c8-8f62-8a603096c097.png)<br/><br/>
2. Search for app<br/>![Search App](https://user-images.githubusercontent.com/87600155/211139605-443c359e-eb6d-4e97-a207-3a05a8efff66.png)<br/><br/>
3. Actual output<br/>![Actual Output](https://user-images.githubusercontent.com/87600155/211139636-07cf3359-9097-45ad-b7fb-7534bf4213ae.png)<br/><br/>
4. Show file content<br/>![show command](https://user-images.githubusercontent.com/87600155/211139661-2c465a10-4548-48e1-8125-623344cff44d.png)<br/><br/>

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

