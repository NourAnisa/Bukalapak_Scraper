import pandas as pd
df = pd.read_json (r'F:/PMB Pasca UIN/Semester 1/Komputasi Sosial/scrapping/data_marketplace.json')
df.to_csv (r'F:/PMB Pasca UIN/Semester 1/Komputasi Sosial/scrapping/data_penjualan.xls', index = None)