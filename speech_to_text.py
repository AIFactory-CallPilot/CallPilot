import whisper

model = whisper.load_model("base")
result = model.transcribe("./[수정]20210123 153723.mp3")
print(result['text'])