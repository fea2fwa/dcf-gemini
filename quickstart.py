import google.generativeai as genai
import os
from dotenv import load_dotenv


load_dotenv()  # .envファイルから環境変数を読み込む
GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)

model = genai.GenerativeModel('gemini-pro')

# response = model.generate_content("日本でDell Technologiesってどう思われている?")

response = model.generate_content('''次の文章を200文字以内で要約して:
          お世話になっております。

Unity300を利用しており、Windowsファイルサーバ（CIFS）として

NASサーバを構成し、WindowsAD認証を行い、ファイルサービスを提供しております。

一部コールセンターを業務を移設することになり、別ネットワークからのアクセスが

必要となり、Unityへ別NetworkのIPを追加設定し、コールセンターからもファイルサーバ

へアクセスできるようにしたいと思っております。

この場合、どのような設定方法によって実現可能でしょうか。

よろしくお願いします。


Unityで対応する場合にはNASサーバに新たなネットワークインタフェースを追加することで対応可能です。
もしも新たなネットワークインタフェースをUnityで設定したくない場合には、IPネットワーク側で別ネットワークからのアクセスを既存のネットワークへ上手くルーティングをさせることでも対応できると思います。


新たなネットワークインタフェースの追加はGUIから ストレージ > ファイル > NASサーバタグ を選択し、該当NASサーバをダブルクリックしてプロパティ画面を表示した後に、「ネットワークタブ」の「ネットワーク インタフェイス」セクションにある「＋」をクリックすることで可能です。
                                  ''')

# for chunk in response:
#   print(chunk.text)
#   print("_"*50)

print(response.text)
