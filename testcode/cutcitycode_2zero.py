import pandas as pd

# CSVファイルを読み込みます
df = pd.read_csv('code_utf8_corrected.csv')

# 列名の空白を取り除きます
df.columns = df.columns.str.strip()

# 列名を表示して確認します
print("Columns:", df.columns)

# 下2桁の0を取り除く関数を定義します
def process_code(code):
    code_str = str(code)
    # 末尾の00を取り除く
    #if code_str.endswith('00'):
    #    code_str = code_str[:-2]
    # 4桁の場合は先頭に0を追加する
    if len(code_str) == 4:
        code_str = '0' + code_str
    return code_str

def process_code2(code):
    code_str = str(code)
    # 末尾の00を取り除く
    #if code_str.endswith('00'):
    #    code_str = code_str[:-2]
    # 4桁の場合は先頭に0を追加する
    if len(code_str) == 6:
        code_str = '0' + code_str
    return code_str

# 対象のCityCode列に対して関数を適用します
if 'areainformationcity_code_s' in df.columns:
    df['areainformationcity_code_s'] = df['areainformationcity_code_s'].apply(process_code)

#if 'areainformationcity_code.1' in df.columns:
#    df['areainformationcity_code.1'] = df['areainformationcity_code.1'].apply(process_code2)

# 結果を新しいCSVファイルに保存します
df.to_csv('code_utf8_corrected.csv', index=False)

# 変更されたデータフレームを表示します
print(df)
