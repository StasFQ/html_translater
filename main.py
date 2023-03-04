import json
import os
import time
import httpcore
import googletrans
import glob
from bs4 import BeautifulSoup
from googletrans import Translator

translator = Translator(service_urls=['translate.google.com'])


def is_translatable(text):
    for char in text:
        if ord(char) > 127:
            return False
    return True


def translate_text(text, max_attempts=3):
    attempts = 0
    while attempts < max_attempts:
        try:
            translated_text = translator.translate(text, dest='hi').text
            return translated_text
        except httpcore._exceptions.ReadTimeout:
            print("ReadTimeout exception occurred. Retrying after 3 seconds...")
            time.sleep(3)
            attempts += 1
        except json.decoder.JSONDecodeError:
            print("JSONDecodeError exception occurred. Retrying after 3 seconds...")
            time.sleep(3)
            attempts += 1
        except AttributeError:
            print("AttributeError exception occurred. Retrying after 3 seconds...")
            time.sleep(3)
            attempts += 1
        except Exception as e:
            print(f"Unknown exception occurred: {e}. Retrying after 3 seconds...")
            time.sleep(3)
            attempts += 1
    print(f"Failed to translate text after {max_attempts} attempts.")
    return None


def translate_html_file(file_path, dest='hi'):
    with open(file_path, 'r+', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        for tag in soup.find_all(string=True):
            if not tag or not tag.strip() or tag.parent.name in ['script', 'style'] or tag.endswith('.com') or tag is None:
                continue
            if is_translatable(tag):
                tag_text = tag.strip()
                if not tag_text.startswith(' '):
                    translated_text = translate_text(tag_text)
                    if translated_text is not None:
                        translated_text = translated_text or ''
                        print(f"{tag} -> {translated_text}")
                        tag.replace_with(translated_text)
    with open(file_path, 'w+', encoding='utf-8') as f:
        f.write(str(soup))


def translate_html_files_in_directory(directory_path):
    html_files = glob.glob(directory_path + '/**/*.html', recursive=True)
    if not html_files:
        print("No HTML files found in the specified directory.")
        return
    for file_path in html_files:
        translate_html_file(file_path)


translate_html_files_in_directory('.')

