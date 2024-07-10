import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from plottable import Table, ColDef
from scipy.stats import ttest_rel, f_oneway
import seaborn as sns
from bs4 import BeautifulSoup

# Assuming fillData function and html paths are already defined as before
# Paths to the HTML files
html = [r"C:\Users\lucas\Desktop\ZJUcamp\Oracle-1.8.0_412-compress\SPECjvm2008.014.html",
        r"C:\Users\lucas\Desktop\ZJUcamp\Alibaba-1.8.0_222-compress\SPECjvm2008.012.html",
        r"C:\Users\lucas\Desktop\ZJUcamp\BiSheng-1.8.0_412-compress\SPECjvm2008.013.html",
        r"C:\Users\lucas\Desktop\ZJUcamp\TencentKona-1.8.0_322-compress\SPECjvm2008.011.html"]


def fillData(html):
    t = np.zeros(shape=(10,))  # Store only the first 10 iterations
    with open(html, 'r', encoding='utf-8') as file:
        content = file.read()
    soup = BeautifulSoup(content, 'html.parser')
    details_table = soup.find_all('table')[10]
    rows = details_table.find_all('tr')[3:]
    i = 0
    for row in rows:
        cols = row.find_all('td')
        if len(cols) == 5:
            t[i] = float(cols[4].text.strip())
            i += 1
    return t

if __name__ == "__main__":
    # Collect data for each JDK
    oracleData = fillData(html[0])
    AlibabaData = fillData(html[1])
    HuaweiData = fillData(html[2])
    TencentData = fillData(html[3])

    jdk_data = pd.DataFrame({
        "Oracle": oracleData,
        "Alibaba": AlibabaData,
        "Huawei": HuaweiData,
        "Tencent": TencentData
    })

    # Visualize data
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=jdk_data)
    plt.title('Performance Distribution of JDKs')
    plt.ylabel('Ops per M')
    plt.show()

    plt.figure(figsize=(12, 6))
    sns.histplot(data=jdk_data, kde=True, multiple="dodge", bins=10)
    plt.title('Histogram of Performance Scores')
    plt.xlabel('Ops per M')
    plt.ylabel('Frequency')
    plt.show()

    # ANOVA
    f_stat, p_value = f_oneway(jdk_data['Oracle'], jdk_data['Alibaba'], jdk_data['Huawei'], jdk_data['Tencent'])
    anova_results = {
        "F-statistic": round(f_stat, 4),
        "p-value": round(p_value, 4),
        "Significant": "Yes" if p_value < 0.05 else "No"
    }
    print("ANOVA Results:", anova_results)
