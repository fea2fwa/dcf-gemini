import pandas as pd

# エクセルファイルを読み込む
df = pd.read_excel('test.xlsx')

print(df.head(10))

# （Windowsだけの問題かもしれない）リンクタグがUTF-8コードのままでブラウザ認識しない箇所を修正するための関数
def convert_entities(text):
    # &lt; を < に置き換え
    text = text.replace("&lt;", "<")
    
    # &gt; を > に置き換え
    text = text.replace("&gt;", ">")

    return text

# E列の値が特定の文字列の場合、F列の文字列にB列のURL情報をHTMLで埋め込む
# for index, row in df.iterrows():
#     if row['Product'] == 'VxRail':
#         row['Summary'] = f'<a href="{row["Thread #"]}">リンク</a>'



# E列の値が「URL」の場合に、F列の文字列にB列のURL情報をHTMLで埋め込む
for i in range(len(df)):
    if df.loc[i, "Product"] == "VxRail":
        df.loc[i, "Summary"] = "<a href=\"{0}\">{1}</a>".format(df.loc[i, "Thread #"], df.loc[i, "Summary"])

df = df.loc[df["Product"] == "VxRail"]

print(df.head(10))

df = df[["Summary"]]
# df = df["Summary"]

print(df.head(10))

# HTMLのテーブル形式で表示する
html = df.to_html(index=False)

# タグを特殊文字から修正
html = convert_entities(html)

html_output = open("htmltext.txt", "w+", encoding="UTF-8")
html_output.write(html)
html_output.close()

# print(html)
