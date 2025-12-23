import re
import time
from pathlib import Path
from deep_translator import GoogleTranslator


# =============================
# 1) 텍스트 전처리 함수
# =============================
def clean_text(text: str) -> str:
    # BOM(눈에 안 보이는 시작 문자) 제거
    text = text.replace("\ufeff", "")
    # zero-width(폭이 0인 이상한 문자) 제거
    text = text.replace("\u200b", "")

    # URL(링크) 제거
    text = re.sub(r"http[s]?://\S+", " ", text)

    # 탭(\t), 캐리지리턴(\r)을 공백으로 치환
    text = re.sub(r"[\r\t]", " ", text)

    # 줄바꿈이 3번 이상 연속되면 2번으로 줄이기
    text = re.sub(r"\n{3,}", "\n\n", text)

    # 느낌표/물음표 제거 (원하면 유지 가능)
    text = text.replace("!", " ").replace("?", " ")

    # 한글/영문/숫자/공백/마침표/줄바꿈만 남기고 나머지는 공백 처리
    text = re.sub(r"[^0-9A-Za-z가-힣\s\.\n]", " ", text)

    # 공백이 2개 이상이면 1개로 줄이기
    text = re.sub(r"[ ]{2,}", " ", text)

    # 줄 끝에 붙은 공백 제거
    text = re.sub(r"[ ]+\n", "\n", text)
    # 줄 시작에 붙은 공백 제거
    text = re.sub(r"\n[ ]+", "\n", text)

    # 앞뒤 공백 제거
    return text.strip()


# =============================
# 2) 문장 후처리
# =============================
def postprocess_sentences(text: str, min_len=1, merge_len=25) -> str:
    # 줄바꿈을 공백으로 바꿔서 문장을 한 줄 흐름으로 만들기
    text = re.sub(r"\s*\n+\s*", " ", text)

    # 공백이 2개 이상이면 1개로 줄이기
    text = re.sub(r"\s{2,}", " ", text).strip()

    # 마침표(.) 기준으로 분리 (양쪽 공백 허용)
    parts = re.split(r"\s*\.\s*", text)

    result = []  # 최종 문장 리스트
    seen = set()  # 중복 제거용

    for part in parts:
        # 문장 양끝 공백 제거
        sent = part.strip()

        # 비어있거나 너무 짧으면 버림
        if not sent or len(sent) < min_len:
            continue

        # 짧은 문장은 직전 문장 뒤에 붙여서 병합
        if len(sent) <= merge_len and result:
            result[-1] = f"{result[-1]} {sent}".strip()
            continue

        # 중복 체크를 위해 공백 정규화한 키 만들기
        key = re.sub(r"\s+", " ", sent)

        # 이미 본 문장이면 건너뜀
        if key in seen:
            continue

        # seen에 등록하고 결과에 추가
        seen.add(key)
        result.append(sent)

    # 문장들을 ".\n"로 이어붙이고 마지막에 마침표 하나 붙이기
    return ".\n".join(result) + ("." if result else "")


# =============================
# 3) 번역 관련 함수
# =============================
def contains_korean(text: str) -> bool:
    # 문자열에 한글이 하나라도 있으면 True
    return any("가" <= ch <= "힣" for ch in text)


def split_text(text: str, max_length=4000):
    # 너무 긴 텍스트를 max_length 기준으로 잘라서 리스트로 반환
    chunks = []
    while len(text) > max_length:
        # max_length 안쪽에서 마지막 공백 위치를 찾아 거기서 자르기
        cut = text.rfind(" ", 0, max_length)

        # 공백이 없으면 그냥 max_length에서 자르기
        if cut == -1:
            cut = max_length

        chunks.append(text[:cut])
        text = text[cut:]

    # 마지막 조각 추가
    chunks.append(text)
    return chunks


def safe_translate(text: str, src="ko", dest="en"):
    # 번역이 실패할 수 있으니 3번까지 재시도
    for attempt in range(3):
        try:
            # GoogleTranslator 객체 생성 (매번 만들어도 되고, 밖에서 재사용해도 됨)
            translator = GoogleTranslator(source=src, target=dest)

            # translate()는 "번역된 문자열"을 바로 반환
            return translator.translate(text)
        except Exception as e:
            # 에러 메시지 출력
            print(f"[ERROR] 번역 실패 ({attempt+1}/3): {e}")

            # 잠깐 쉬었다가 재시도
            time.sleep(3)

    # 3번 다 실패하면 빈 문자열 반환
    return ""


# =============================
# 4) 핵심 로직
# =============================
def merge_preprocess_translate(
    input_dir: str,
    cleaned_output_file: str,
    translated_output_file: str,
):
    # 입력 폴더 경로를 Path 객체로 변환
    input_path = Path(input_dir)

    # 폴더 안의 txt 파일 목록 가져오기 (이름 순 정렬)
    txt_files = sorted(input_path.glob("*.txt"))

    # txt 파일이 없으면 종료
    if not txt_files:
        print("폴더에 txt 파일이 없습니다.")
        return

    print(f"텍스트 파일 {len(txt_files)}개 병합 시작")

    # 1) 모든 파일 병합
    merged_texts = []
    for file in txt_files:
        print(f"병합 중: {file.name}")
        # 파일 내용을 읽어서 리스트에 추가 (인코딩 에러 무시)
        merged_texts.append(file.read_text(encoding="utf-8", errors="ignore"))

    # 리스트를 줄바꿈으로 연결해서 하나의 큰 텍스트 만들기
    merged_text = "\n".join(merged_texts)
    print(f"병합 후 길이: {len(merged_text)}자")

    # 2) 전처리
    cleaned = clean_text(merged_text)
    cleaned = postprocess_sentences(cleaned)
    print(f"전처리 후 길이: {len(cleaned)}자")

    # 3) 전처리본 저장
    Path(cleaned_output_file).write_text(cleaned, encoding="utf-8")
    print(f"전처리본 저장: {cleaned_output_file}")

    # 4) 번역
    if not contains_korean(cleaned):
        # 한글이 없으면 번역할 필요 없음
        print("한글 없음 → 번역 생략")
        final_text = cleaned
    else:
        # 너무 길면 쪼개서 번역
        chunks = split_text(cleaned, max_length=2000)
        translated_chunks = []

        for i, chunk in enumerate(chunks):

            print(f" 번역 중... ({i+1}/{len(chunks)})")
            translated_chunks.append(safe_translate(chunk, src="ko", dest="en"))
            time.sleep(1)  # 너무 빠른 요청 방지

        # 번역된 조각을 합치기
        final_text = "\n".join(translated_chunks)


    # 5) 번역본 저장
    Path(translated_output_file).write_text(final_text, encoding="utf-8")
    print(f"번역본 저장: {translated_output_file}")
    print(f"최종 길이: {len(final_text)}자")

# =============================
# 실행부
# =============================
if __name__ == "__main__":
    merge_preprocess_translate(
        input_dir=r"C:\work\K리그_모음\Ulsan_HD",                 # 예: r"C:\data\texts"   # 번역할 폴더
        cleaned_output_file=r"C:\work\K리그_모음\전처리\울산_전처리.txt",        # 예: r"C:\data\out\cleaned.txt" # 전처리만하는 경로
        translated_output_file=r"C:\work\K리그_모음\번역\울산_전처리_번역.txt",     # 예: r"C:\data\out\translated.txt"`# 전처리 + 번역까지`
    )

