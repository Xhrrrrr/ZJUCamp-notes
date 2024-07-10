import matplotlib
import numpy as np
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
from plottable import Table, ColDef

html = [r"C:\Users\lucas\Desktop\ZJUcamp\Oracle-1.8.0_412-compress\SPECjvm2008.014.html",
        r"C:\Users\lucas\Desktop\ZJUcamp\Alibaba-1.8.0_222-compress\SPECjvm2008.012.html",
        r"C:\Users\lucas\Desktop\ZJUcamp\BiSheng-1.8.0_412-compress\SPECjvm2008.013.html",
        r"C:\Users\lucas\Desktop\ZJUcamp\TencentKona-1.8.0_322-compress\SPECjvm2008.011.html"]

def fillData(html):
    t = np.zeros(shape=(1, 12))
    # 读取HTML文件内容
    with open(html, 'r', encoding='utf-8') as file:
        content = file.read()

    # 解析HTML内容
    soup = BeautifulSoup(content, 'html.parser')

    # 找到"Details of Runs"表格
    details_table = soup.find_all('table')[10]  # 第10个表格是我们需要的
    # print(details_table)

    # 提取表格中的行
    rows = details_table.find_all('tr')[3:]  # 从第四行开始是数据行
    # print(rows)

    iteration_data = []
    i = 0
    for row in rows:
        cols = row.find_all('td')
        # print(cols)
        if len(cols) == 5:  # 忽略其他行，只处理包含所有数据的行
            iteration = cols[0].text.strip()
            expected_run_time = cols[1].text.strip()
            actual_run_time = cols[2].text.strip()
            operations = cols[3].text.strip()
            ops_per_m = cols[4].text.strip()
            iteration_data.append({
                'iteration': iteration,
                'expected_run_time': expected_run_time,
                'actual_run_time': actual_run_time,
                'operations': operations,
                'ops_per_m': ops_per_m
            })
            t[0][i] = float(cols[4].text.strip())
            i += 1

    # 打印提取的信息
    # for data in iteration_data:
        # print(data)
    mean = np.mean(t[0][:10])
    t[0][10] = mean
    std = np.std(t[0][:10])
    t[0][11] = std
    # print(t)
    return t




if __name__ == "__main__":

    oracleData = fillData(html[0])
    AlibabaData = fillData(html[1])
    HuaweiData = fillData(html[2])
    TencentData = fillData(html[3])

    col = [f"iteration {i}" for i in range(1, 11)]
    col.append("mean")
    col.append("std")
    stacked_vertically = np.vstack((oracleData, AlibabaData, HuaweiData, TencentData))
    data = pd.DataFrame(
        data=stacked_vertically,
        columns=col
    )
    data = data.rename(index={0: "Oracle", 1 : "Alibaba", 2: "Huawei", 3: "Tencent"})
    data = data.round(2)
    fig, ax = plt.subplots()
    Table(
        data,
        textprops={
            "ha" : "center"
        },
        column_definitions=[
            ColDef(name="std", text_cmap=matplotlib.cm.Greens)
        ])

    plt.show()




