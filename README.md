# CallPilot - LLM 기반 상담내용 자동요약 서비스

공고: https://aifactory.space/competition/detail/2376
- 서울시생성AI해커톤 - 120다산콜센터 부문.


## product 설명

### upload

gcp Cloud Functions으로 배포
- input: HTTP Post, multipart/form-data 형식으로 audio/mp3 파일을 request
- process: processing metadata를 cloud firestore에, audio 파일을 cloud storage에 저장
- output: status 200, storage와 filestore에 저장된 filename

### stt-by-api

gcp cloud Functions으로 배포
- input: storage의 file upload 이벤트
- process: OpenAI Whipser API로 Speech to text 로직 수행, Speech to text 결과를 cloud firestore에 저장
- output: status 200

### summarize-llm

gcp cloud run으로 배포 (Dockerfile)
- input: cloud workflow에서 stt-by-api 수행 이후 다음 프로세스로 실행됨
- process: speech to text 결과로 나온 텍스트를 OpenAI ChatGPT API로 요약 요청, cloud firestore에 요약 결과 저장
- output: status 200

### get-response

gcp cloud run으로 배포 (Dockerfile)
- input: path parameter로 upload에서 응답받은 filename
- process: cloud firestore에서 metadata를 조회
- output: cloud firestore에 저장된 값
  - name: mp3 파일명
  - summary: 요약 결과
  - text: speech to text 결과물
  - process: 진행 상황
