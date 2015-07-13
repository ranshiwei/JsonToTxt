# JsonToTxt
本脚本JsonTT-V4用于处理指定格式的json文件，通过读取用户输入的文件路径或者是文件夹路径，将指定的json文件或文件下的所有json文件，转化为根据host划分的txt文件。
本版本处理的json文件格式实例：
{"host":"205.234.131.206",
"domain":null,
"time":"2015-07-03T16:00:10-04:00",
"log":[{"type":"connect","data":null,"error":null},
{"type":"read","data":{"response":"220 Welcome to Pure-FTPd [privsep] [TLS] "},"error":null}]}
（若需要修改json格式，只需修改createTxt函数中相应读取字段值）

本脚本根据用户输入的文件路径或文件夹路径，在相应路径下自动生成文件夹JsonToTxt，并将转化后的txt文件自动存到该文件夹下。
