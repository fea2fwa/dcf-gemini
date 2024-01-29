import requests
from bs4 import BeautifulSoup
import json

url = "https://www.dell.com/community/ja/conversations/%E3%82%B9%E3%83%88%E3%83%AC%E3%83%BC%E3%82%B8-%E3%82%B3%E3%83%9F%E3%83%A5%E3%83%8B%E3%83%86%E3%82%A3/vxrail%E3%81%AEvsan-max%E6%A7%8B%E6%88%90%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6/65af42cb66067b0d2e9e52cd"
# url = "https://www.dell.com/community/ja/conversations/%E3%82%B9%E3%83%88%E3%83%AC%E3%83%BC%E3%82%B8-%E3%82%B3%E3%83%9F%E3%83%A5%E3%83%8B%E3%83%86%E3%82%A3/powerflex%E3%81%AE%E5%9F%BA%E6%9C%AC%E6%A7%8B%E6%88%90%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6/65b0866fa51f722bfe7fb348"
# url = "https://www.dell.com/community/ja/conversations/%E3%82%B9%E3%83%88%E3%83%AC%E3%83%BC%E3%82%B8-%E3%82%B3%E3%83%9F%E3%83%A5%E3%83%8B%E3%83%86%E3%82%A3/unity-xt-destination%E5%81%B4snapshot%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%97%E3%81%A6source%E5%81%B4%E3%81%AE%E4%B8%96%E4%BB%A3%E7%AE%A1%E7%90%86%E3%82%92%E8%A1%8C%E3%81%86/65a73d32792ba45dca625e95"

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


    print(question_text)

    # 複数エントリーがある場合のためにリスト化したコンテンツを表示
    for content in suggested_answer_text:
        cleaned_text =convert_entities(content)
        print(cleaned_text)    

    # 複数エントリーがある場合のためにリスト化したコンテンツを表示
    for content in accepted_answer_text:
        cleaned_text = convert_entities(content)
        print(cleaned_text)


fetch_data_from_url(url)