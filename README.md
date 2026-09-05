---
title: End-to-End Video Streaming & RecSys Lab
aliases:
  - Streaming RecSys Lab
  - 스트리밍 추천 랩
tags:
  - MOC
  - video-streaming
  - recsys
created: 2026-09-02
---

# End-to-End Video Streaming & RecSys Lab

> [!abstract] 이 볼트에 대하여
> 영상 인코딩, HLS 스트리밍 파이프라인부터 딥러닝 기반 추천 알고리즘까지 엔지니어링 전체 과정을 학습하고 기록하는 아카이브

---

## 📒 노트

### [[ffmpeg, 스트리밍 기초]]

코덱·컨테이너부터 브라우저 재생까지 스트리밍 파이프라인의 기초.

- [[ffmpeg, 스트리밍 기초#1. 코덱 & 컨테이너 (Codec / Container)|코덱 & 컨테이너]] — H.264/H.265/AV1 트레이드오프, 확장자 ≠ 코덱
- [[ffmpeg, 스트리밍 기초#2. 프레임 구조와 GOP (Group of Pictures)|프레임 구조와 GOP]] — I/P/B, GOP 길이와 세그먼트 정렬
- [[ffmpeg, 스트리밍 기초#3. 비트레이트 제어 — '얼마나'가 아니라 '어떻게' 쓸지|비트레이트 제어]] — CBR/VBR/CRF, VBV 상한, ABR 래더 설계
- [[ffmpeg, 스트리밍 기초#4. HLS 및 가변 비트레이트 (ABR: Adaptive Bitrate Streaming)|HLS & ABR]] — 플레이리스트 2종, 전환은 다음 조각부터
- [[ffmpeg, 스트리밍 기초#5. FFmpeg 파이프라인에서 실제로 하는 일|FFmpeg 파이프라인]] — ABR 패키징 명령어, `ffprobe` 검증
- [[ffmpeg, 스트리밍 기초#6. 웹 클라이언트 재생 — 서버 인코딩과는 다른 층|웹 클라이언트 재생]] — CORS, MSE/`hls.js`, 디버깅 4단계

---

## 🧪 실습 산출물 (`FFmpeg/`)

| 파일                                      | 확인한 것                                 |
| --------------------------------------- | ------------------------------------- |
| `sample.mp4`                            | 원본 소스                                 |
| `output_low.mp4`                        | 해상도·비트레이트 다운스케일                       |
| `output_crf18.mp4` / `output_crf32.mp4` | CRF 값에 따른 화질·용량 차이 (1.73MB ↔ 0.67MB)  |
| `output_gop60.mp4`                      | `-g 60` → 2초 간격 키프레임 (`ffprobe`로 검증)  |
| `index.m3u8` + `segment_00*.ts`         | 단일 비트레이트 HLS 세그먼팅                     |
| `master.m3u8` + `v0/` `v1/` `v2/`       | ABR 3트랙 패키징 (1080p / 720p / 480p)     |
| `index.html`                            | `hls.js` 기반 웹 플레이어 (`master.m3u8` 재생) |
| `thumbnail.jpg`                         | 특정 시점 프레임 추출                          |


> [!warning] 미디어 파일은 Git에 포함되지 않음
> `.mp4` · `.ts`는 `.gitignore` 대상이라 저장소에는 **플레이리스트(`.m3u8`) · 플레이어(`.html`) · 썸네일만** 올라간다.
> 클론 후 재생하려면 원본 영상을 `FFmpeg/sample.mp4`로 두고 [[ffmpeg, 스트리밍 기초#5. FFmpeg 파이프라인에서 실제로 하는 일|노트의 패키징 명령어]]를 다시 실행할 것.

> [!note] 로컬 재생 방법
> `file://`로 열면 CORS에 막히므로 `FFmpeg/` 안에서 `python -m http.server 8000` 실행 후 `http://localhost:8000` 접속.

---

## 🗺️ 로드맵

### Part 1. 비디오 스트리밍 파이프라인

- [x] **비디오 인코딩 및 코덱 기초** → [[ffmpeg, 스트리밍 기초]]
  - [x] FFmpeg CLI 기본 사용법 익히기
  - [x] 비디오/오디오 코덱(H.264, AAC) 및 컨테이너(MP4, TS) 차이 이해
  - [x] 해상도, FPS, 비트레이트(Bitrate), GOP/Keyframe 개념 정리
- [x] **프로토콜 및 가변 비트레이트 (ABR)**
  - [x] HLS (HTTP Live Streaming) 구조 파악 (`.m3u8` 파일 및 `.ts` 세그먼트)
  - [x] FFmpeg로 단일 `.mp4` 영상을 다중 비트레이트 HLS 세그먼트로 변환
- [x] **웹 플레이어 연동 및 보안** 
  - [x] HTML5 + `hls.js` 기반 웹 미디어 플레이어 구현
  - [x] 이벤트 수집 기초 [[웹 플레이어 연동 및 이벤트 수집]]
  - [ ] 시청 시간, 완독률, 클릭 이벤트를 백엔드로 전송하는 이벤트 핸들러 작성
- [ ] **스트리밍 백엔드 & 비동기 파이프라인**
  - [ ] Python 백엔드(FastAPI 등) 기반 비동기 작업 큐(Redis/Celery) 구축
  - [ ] 유저 업로드 → HLS 변환 → 저장소(S3/Local) 업로드 자동화

### Part 2. 추천 시스템

- [ ] **기초 수학 & 데이터 전처리**
  - [ ] 선형대수 핵심 복습 (행렬 곱, 내적, 코사인 유사도)
  - [ ] Pandas/NumPy 기반 시청 로그 데이터 가공
  - [ ] 평가 지표 이해 (Precision@K, Recall@K, NDCG)
- [ ] **전통적 추천 알고리즘 (Machine Learning)**
  - [ ] 콘텐츠 기반 필터링 (Content-based Filtering) 구현
  - [ ] 협업 필터링 (User-based / Item-based CF) 구현
  - [ ] 행렬 분해 (Matrix Factorization, SVD) 및 Implicit Feedback 처리
- [ ] **영상 특화 멀티모달 & 시청 Signal 정제**
  - [ ] 썸네일/텍스트/오디오 데이터의 임베딩 추출 파이프라인
  - [ ] 완독률(Completion Rate), 시청 시간 기반의 Target Label 설계
- [ ] **딥러닝 기반 추천 (Deep Learning)**
  - [ ] PyTorch 기초 및 신경망(MLP) 구성
  - [ ] **YouTube 2-Stage Architecture 분석 및 구현**
    - [ ] Candidate Generation (Two-Tower Model / Vector Embedding)
    - [ ] Ranking (Deep & Cross Network / Multi-task Learning)
  - [ ] 시퀀셜 추천 (SASRec 등 최근 시청 순서 반영 모델)
- [ ] **실무 서빙 & 검색 엔지니어링**
  - [ ] 대용량 벡터 검색 (FAISS / HNSW) 기반 Top-K 추출 구현
  - [ ] Exploration vs Exploitation (Multi-Armed Bandit) 기초 적용

---

> [!todo] 다음 할 일
> 1. `index.html`에 **시청 이벤트 핸들러** 추가 — `timeupdate`로 시청 구간, `ended`로 완독률, 화질 전환 로그 수집
> 2. 수집한 이벤트를 받을 **FastAPI 엔드포인트** + 비동기 변환 큐(Celery) 구성
> 3. 쌓인 시청 로그를 Part 2의 **추천 학습 데이터**로 연결
