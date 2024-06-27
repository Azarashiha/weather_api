import pandas as pd

# CSVファイルの読み込み
input_file = 'code_utf8_corrected.csv'
output_file = 'code_utf8_corrected.csv'

# CSVファイルをDataFrameに読み込む
df = pd.read_csv(input_file, encoding='utf-8')

# 列名の修正
df.columns = [
    'areaforecastlocale_code', 
    'areaforecastlocale_name', 
    'areaforecastlocale_kana', 
    'areainformationcity_code', 
    'areainformationcity_code_s', 
    'areainformationcity_name', 
    'areainformationcity_kana', 
    'pointseismicintensity_code', 
    'pointseismicintensity_name', 
    'pointseismicintensity_kana'
]

# pointseismicintensity_code 列のデータ型を修正
df['pointseismicintensity_code'] = pd.to_numeric(df['pointseismicintensity_code'], errors='coerce')

# areainformationcity_code_s 列を修正する関数
def process_code(code):
    code_str = str(code)
    # 4桁の場合は先頭に0を追加する
    if len(code_str) == 4:
        code_str = '0' + code_str
    # 6桁の場合は最後の文字を削除する
    elif len(code_str) == 6:
        code_str = code_str[:-1]
    return code_str

# 対象の areainformationcity_code_s 列に対して関数を適用
if 'areainformationcity_code_s' in df.columns:
    df['areainformationcity_code_s'] = df['areainformationcity_code_s'].apply(process_code)

# データの内容を確認（オプション）
print(df)

# 修正されたデータを新しいCSVファイルに保存
df.to_csv(output_file, index=False, encoding='utf-8')

print(f'修正されたファイルが {output_file} に保存されました')
