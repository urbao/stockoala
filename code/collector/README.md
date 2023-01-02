# stock_collector
## Fullname
--Taiwan Stock Collect with Python<br />
## Compile Environment
--Ubuntu 22.04 64(bit)<br />
--Python 3.10.6<br />
--Micro text editor<br />
## Way to Use
--Enter the Monday date, and Default collect 5 days data<br/>
--TWSE and TPEX stock data is all collected<br/>
--All data is stored into a file same name with Monday date<br/>
## Additional
### If we want to change collected date from 5 days to 6 days, follow below instructions:
--1.Change line 15 in main.py from "for i in range(5)" to "for i in range(6)"<br/>
--2.Change line 124 in parse.py from "for i in range(4)" to "for i in range(5)"<br/><br/>
Stock data parser: https://github.com/urbao/stock_parser <br/>
Stock data storage: https://github.com/urbao/stock_data<br/>
