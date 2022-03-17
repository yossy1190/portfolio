
import eel
import desktop
import pandas as pd
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# eel_projectの直下にhtmlフォルダあり
app_name="html"
# htmlフォルダの直下にあるindex.htmlを参照
end_point="index.html"
size=(700,600)


def set_driver(hidden_chrome: bool=False):
    '''
    Chromeを自動操作するためのChromeDriverを起動してobjectを取得する
    '''
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）の設定
    options.add_argument('--headless')

    # その他起動オプションの設定
    options.add_argument(f'--user-agent={USER_AGENT}') # ブラウザの種類を特定するための文字列
    options.add_argument('log-level=3') # 不要なログを非表示にする
    options.add_argument('--ignore-certificate-errors') # 不要なログを非表示にする
    options.add_argument('--ignore-ssl-errors') # 不要なログを非表示にする
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # 不要なログを非表示にする
    options.add_argument('--incognito') # シークレットモードの設定を付与
    
    # ChromeのWebDriverオブジェクトを作成する。
    service=Service(ChromeDriverManager().install())
    return Chrome(service=service, options=options)

@eel.expose
def search_word(search_word,csv_name):
    # Webサイトを開く
    # search のあとに、system や webなどをくっつけること遷移可能    
    driver=set_driver()
    driver.get("https://www.lancers.jp/work/search/")
    
    time.sleep(2)
   
    try:
        driver.execute_script('document.querySelector(".Commonstyled__PreviewCloseButton-sc-1uivlpa-3.jOVdaf").click()')
        time.sleep(5)
    except:
        print("ポップアップなし")
    '''
    キーワード検索
    '''
    driver.find_element(by=By.ID, value="Keyword").send_keys(search_word)
    driver.find_element(by=By.ID, value="Search").click()
    time.sleep(1.0)

    job_items=[]    
    while True:
        title_elms= driver.find_elements(by=By.CLASS_NAME, value="c-media__title-inner")
        payment_elms=driver.find_elements(by=By.CLASS_NAME,value="c-media__job-price")
        propose_elms=driver.find_elements(by=By.CLASS_NAME ,value="c-media__title")
            
        for title_elm,payment_elm,propose_elm, in zip(title_elms,payment_elms,propose_elms):
            
            propose_link=propose_elm.get_attribute("href")
            print(title_elm.text,payment_elm.text)
            # DataFrameに対して辞書形式でデータを追加する
            job_items.append(
                {"案件名": title_elm.text, 
                "報酬額": payment_elm.text,
                "案件リンク":propose_link
                }, 
                )
        
        try:
            driver.find_element(by=By.CLASS_NAME, value="pager__item--next").click()
            time.sleep(0.5)
        except:
            print("最終ページです。")
            break
        
    df=pd.DataFrame.from_dict(job_items,dtype=object)
    df.index=df.index+1
    df.to_csv(f"{csv_name}.csv",encoding="utf_8_sig")
    
desktop.start(app_name,end_point,size)

