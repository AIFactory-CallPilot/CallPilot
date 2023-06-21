import glob
import os

import whisper

import aws_client
from speech_to_text import speech_to_text

if __name__ == "__main__":
    model = whisper.load_model("small")
    category_name = "생활하수도 관련 문의"
    # category_name = os.environ["category"]  # 환경변수로 category 설정
    files = glob.glob(os.path.join(os.getcwd(), "training", category_name, "*.mp3"))
    for path in files:
        print(path)
        filename = os.path.basename(path)
        text = speech_to_text(model, path)
        print(text)
        response = aws_client.dynamoDB_put_item('voice_to_text', filename, text, category_name, "training")


