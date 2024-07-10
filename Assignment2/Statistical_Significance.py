import matplotlib
import numpy as np
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
from plottable import Table, ColDef
from scipy.stats import ttest_rel  # Import for paired t-tests

# Paths to the HTML files
html = [r"C:\Users\lucas\Desktop\ZJUcamp\Oracle-1.8.0_412-compress\SPECjvm2008.014.html",
        r"C:\Users\lucas\Desktop\ZJUcamp\Alibaba-1.8.0_222-compress\SPECjvm2008.012.html",
        r"C:\Users\lucas\Desktop\ZJUcamp\BiSheng-1.8.0_412-compress\SPECjvm2008.013.html",
        r"C:\Users\lucas\Desktop\ZJUcamp\TencentKona-1.8.0_322-compress\SPECjvm2008.011.html"]


def fillData(html):
    t = np.zeros(shape=(1, 12))
    with open(html, 'r', encoding='utf-8') as file:
        content = file.read()
    soup = BeautifulSoup(content, 'html.parser')
    details_table = soup.find_all('table')[10]
    rows = details_table.find_all('tr')[3:]
    i = 0
    for row in rows:
        cols = row.find_all('td')
        if len(cols) == 5:
            t[0][i] = float(cols[4].text.strip())
            i += 1
    mean = np.mean(t[0][:10])
    t[0][10] = mean
    std = np.std(t[0][:10])
    t[0][11] = std
    return t


if __name__ == "__main__":
    oracleData = fillData(html[0])
    AlibabaData = fillData(html[1])
    HuaweiData = fillData(html[2])
    TencentData = fillData(html[3])

    # Perform paired t-tests
    oracle = oracleData[0][:10]
    alibaba = AlibabaData[0][:10]
    huawei = HuaweiData[0][:10]
    tencent = TencentData[0][:10]


    # Create a function to perform paired t-tests and store results
    def perform_ttest(data1, name1, data2, name2):
        t_stat, p_value = ttest_rel(data1, data2)
        result = {
            "Comparison": f"{name1} vs {name2}",
            "t-statistic": round(t_stat, 4),
            "p-value": round(p_value, 4),
            "Significant": "Yes" if p_value < 0.05 else "No"
        }
        return result


    # List to store t-test results
    ttest_results = []

    # Perform t-tests between each pair of JVMs
    ttest_results.append(perform_ttest(oracle, "Oracle", alibaba, "Alibaba"))
    ttest_results.append(perform_ttest(oracle, "Oracle", huawei, "Huawei"))
    ttest_results.append(perform_ttest(oracle, "Oracle", tencent, "Tencent"))
    ttest_results.append(perform_ttest(alibaba, "Alibaba", huawei, "Huawei"))
    ttest_results.append(perform_ttest(alibaba, "Alibaba", tencent, "Tencent"))
    ttest_results.append(perform_ttest(huawei, "Huawei", tencent, "Tencent"))

    # Convert results to DataFrame
    ttest_df = pd.DataFrame(ttest_results)

    # Display t-test results as a table
    fig, ax = plt.subplots()
    Table(
        ttest_df,
        textprops={"ha": "center"}
    )

    plt.show()

    # Print t-test results as a table
    print(ttest_df)
