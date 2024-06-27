import csv

# 入力と出力のCSVファイル名
input_file = 'code_utf8.csv'
output_file = 'code_addzero1_utf8.csv'

# CSVファイルを読み込んで書き込む

with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # ヘッダーを読み込む
        headers = next(reader)
        
        # 新しいヘッダーを作成する
        new_headers = []
        for header in headers:
            new_headers.append(header)
            if header == 'areainformationcity_code':
                new_headers.append('areainformationcity_code_s')
        
        # 新しいヘッダーを書き込む
        writer.writerow(new_headers)
        
        # データ行を処理する
        for row in reader:
            new_row = []
            for i, value in enumerate(row):
                new_row.append(value)
                if headers[i] == 'areainformationcity_code':
                    new_row.append(str(value))  # areainformationcity_code_sとして追加
            
            # 新しい行を書き込む
            writer.writerow(new_row)
    
print("新しいCSVファイルが保存されました。")


