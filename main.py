from googletrans import Translator
from bs4 import BeautifulSoup
import os


translator = Translator()


source_lang = input("Введіть мову, з якої потрібно перекласти текст: ")


target_lang = input("Введіть мову, на яку потрібно перекласти текст: ")


html_folder_path = input("Введіть шлях до теки з HTML файлами: ")


for filename in os.listdir(html_folder_path):
    if filename.endswith(".html"):
        file_path = os.path.join(html_folder_path, filename)

        with open(file_path, "r") as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")

        for tag in soup.find_all(text=True):
            if tag.parent.name not in ['script', 'style']:
                translation = translator.translate(tag, src=source_lang, dest=target_lang)
                tag.replace_with(translation.text)

        with open(file_path, "w") as f:
            f.write(str(soup))




