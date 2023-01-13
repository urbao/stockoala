
# Stockoala

Combine functionality of Collect/Analyze Taiwan stock data together running via terminal<br/><br/>

![Logo](https://cdn-icons-png.flaticon.com/128/424/424783.png)

## Features

- collect `TWSE and TPEX` stock data by user specific period(`ID`/`High`/`Low`/`Open`/`Close`/`Transaction`)
- check which stock is at `Reverse Point` for the most recent date
- push all data and result to GitHub `(Backup Purpose)`

## Run Locally

Clone the project
```bash
git clone git@github.com:urbao/stockoala.git
```

Go to the project directory
```bash
cd "DIRECTORY_PATH"
```

Remove original .git/ dir & data/ dir
```bash
rm -rf .git/ data/
```

Create .gitignore file, so only necessary files pushed to GitHub
```bash
{ echo __pycache__/; echo "*.py"; echo "*.sh"; } >> .gitignore
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

Make installation file executable
```bash
chmod +x install.sh
```

Start install process
```bash
./install.sh
```

Finally, You are good to go~<br/>


## Appendix

- **Default value  of 'install.sh'** can be modified based on personal preference<br/>
- For examples, **dirpath** can be changed from `"$HOME/Desktop/stockoala"` to `"$HOME/Documents/stockoala"` depends on you<br/>
- And, `dsktpath`, `iconpath` and `usrname` can also be done just like this<br/>
- **HOWEVER, make sure the path is valid!!!**
## Screenshots

### 1. Installation<br/>![Installation](https://user-images.githubusercontent.com/87600155/211139578-d6650af4-8c76-46c8-8f62-8a603096c097.png)<br/><br/>
### 2. Search for app<br/>![Search App](https://user-images.githubusercontent.com/87600155/211139605-443c359e-eb6d-4e97-a207-3a05a8efff66.png)<br/><br/>
### 3. Actual output<br/>![Actual Output](https://user-images.githubusercontent.com/87600155/211139636-07cf3359-9097-45ad-b7fb-7534bf4213ae.png)<br/><br/>
### 4. Collecting data<br/>![image](https://user-images.githubusercontent.com/87600155/211968676-73bde77f-02ca-4cb5-a7b3-24051d969979.png)<br/>br/>
### 5. Prune data files<br/>![image](https://user-images.githubusercontent.com/87600155/211968821-14dd52b7-259d-491a-b32e-3efedf02e1c6.png)<br/><br/>
### 6. Parsing data<br/>![image](https://user-images.githubusercontent.com/87600155/211968933-48c385a1-d7b6-479d-af05-e912028a817f.png)<br/>
![image](https://user-images.githubusercontent.com/87600155/211968952-2a191770-110f-4e4d-ab55-0bd5c28387e6.png)


## Related

Here are some related stock market official link

[Taiwan Stock Exchange](https://www.twse.com.tw/zh/page/trading/exchange/STOCK_DAY.html)<br/>
[Taipei Exchange](https://www.tpex.org.tw/web/stock/aftertrading/daily_trading_info/st43.php?l=zh-tw)<br/>

## FAQ

#### Question 1: What's the structure of whole project?<br/>

Ans: Use Python and Bash to collect given period **Taipei Exchange and Taiwan Stock Exchange data**, and the `Python` does the most job of `collecting and parsing`, while `Bash` controls the `workflow and the fileviewer task`<br/>
#### Question 2: Can this project run on Windows?<br/>

Ans: Maybe, It depends on condition of your PC.<br/> If **Windows Subsystem for Linux and Python3** is installed, it might works. The *ONLY* thing that is for sure is `Running on Ubuntu 22.04 works well`<br/> 

## Authors

- [@urbao](https://www.github.com/urbao)


## Feedback

If you have any feedback, please reach out to us at zardforever1009@gmail.com

