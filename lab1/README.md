# CDR (Call Detail Record)
<img src="./img/Capture.png" alt="" width="300"/>

```
.
├── img\
├── report\
├── cdr.py
├── data.scv
├── parse.py
└── tariffing.py
```
### Description
Программа для тарификации абонентов с заданным тарифом при помощи файла с CDR в формате .csv. 

### Run
Для запуска необходим Python любой версии, используются только стандартные его библиотеки.
```
python ./cdr.py
```
### Input files
По умолчанию программа будет искать файл с CDR как `data.scv`.