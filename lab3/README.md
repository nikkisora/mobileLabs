# Payment document
<img src="./img/Capture.png" alt="" width="300"/>

```
.
├── img\
├── report\
├── blank.html
├── compileInvoice.py
├── Filled.pdf
└── num2text.py
```
### Description
Программа для создания отчёта о тарификации абонентов. 

### Run
Для запуска программы необходим:
- Python3 с библиотекой `weasyprint` и `BeautifulSoup`
```
pip install weasyprint
pip install bs4
```

### Input/Output files
Программа изначально запускает предыдущие два проекта, соответственно, они должны быть склонированы из репозитория и на ходиться на уровень выше:
```
.
├── lab1
├── lab2
└── lab3
    └── compileInvoice.py
```
Необходимы файлы `clean_data.csv` в директории `lab2`, `data.csv` в директории `lab1` и `blank.html` в директории `lab3`.

По окончании работы программа создаёт отчёт с названием `Filled.pdf` в директории `lab3`.