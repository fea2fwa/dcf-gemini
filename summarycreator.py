import google.generativeai as genai
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd


load_dotenv()  # .envファイルから環境変数を読み込む
GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

def convert_entities(text):
    # 不要な単語をリスト
    special_charactors = ["&nbsp;", "&gt;"]

    # 不要な単語を削除
    for character in special_charactors:
        text = text.replace(character, "")
    
    return text

def fetch_data_from_url(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser') 

    # criptタグのtype "application/ld+json"からコンテンツを入手
    script_content = soup.find('script', {'type': 'application/ld+json'}).string

    # コンテンツをJSON形式でload、特殊文字が入っているのでstrict=Falseを設定
    json_data = json.loads(script_content, strict=False)

    # JSONデータからmainEntityのtextを抜き出し
    try:
        question_text = json_data["mainEntity"]["text"]
    except:
        question_text = None

    try:
        suggested_answer_text = []
        if isinstance(json_data["mainEntity"]["suggestedAnswer"], dict): # ディクショナリの場合の処理
            suggested_answer_text.append(json_data["mainEntity"]["suggestedAnswer"]["text"])
        
        elif isinstance(json_data["mainEntity"]["suggestedAnswer"], list): # リストの場合の処理
            for answer in json_data["mainEntity"]["suggestedAnswer"]:
                suggested_answer_text.append(answer["text"])    
        else:
            print("No suggested answer found.")
    except Exception as e:
        print(f"suggested answer取得に失敗したか、該当項目が存在しませんでした：{e}")

    try:
        accepted_answer_text = []
        if isinstance(json_data["mainEntity"]["acceptedAnswer"], dict): # ディクショナリの場合の処理
            accepted_answer_text.append(json_data["mainEntity"]["acceptedAnswer"]["text"])
        
        elif isinstance(json_data["mainEntity"]["acceptedAnswer"], list): # リストの場合の処理
            for answer in json_data["mainEntity"]["acceptedAnswer"]:
                accepted_answer_text.append(answer["text"])    
        else:
            print("No accepted answer found.")
    except Exception as e:
        print(f"accepted answer取得に失敗したか、該当項目が存在しませんでした：{e}")

    whole_text = ""
    whole_text += "[質問]"
    whole_text += question_text
    whole_text += "[提案された回答]"

    for content in suggested_answer_text:
        cleaned_text =convert_entities(content)
        whole_text += cleaned_text
    
    whole_text += "[受け入れられた良い回答]"
    
    for content in accepted_answer_text:
        cleaned_text = convert_entities(content)
        whole_text += cleaned_text
    
    return(whole_text)


def main():
    # エクセルファイルを読み込む
    df = pd.read_excel('test.xlsx')

    # VxRailに関するコンテンツのみを抽出
    df = df.loc[df["Product"] == "VxRail"]

    # df_summary = pd.DataFrame(columns=["Summary (AI generated)"])
    summary_list = []
    for url in df["Thread #"]:
        
        row_text = fetch_data_from_url(url)
        response = model.generate_content(f"次の文章を200文字以内で要約して:{row_text}")
        print(response.text)
        summary_list.append(response.text)

    df_summary = pd.DataFrame({"Summary (AI generated)": summary_list})                                      
    print(df_summary.head(20))

if __name__ == "__main__":
    main()
