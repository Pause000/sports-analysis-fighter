import re
import time
from pathlib import Path
from googletrans import Translator


# =============================
# 1) 텍스트 전처리 함수
# =============================
def clean_text(text: str) -> str:
    text = text.replace("\ufeff", "")              # BOM 제거
    text = text.replace("\u200b", "")              # zero-width 문자 제거
    text = re.sub(r"http[s]?://\S+", " ", text)    # URL 제거
    text = re.sub(r"[\r\t]", " ", text)            # \r, \t 제거
    text = re.sub(r"\n{3,}", "\n\n", text)         # 줄바꿈 정리
    text = text.replace("!", " ").replace("?", " ")
    text = re.sub(r"[^0-9A-Za-z가-힣\s\.\n]", " ", text)
    text = re.sub(r"[ ]{2,}", " ", text)
    text = re.sub(r"[ ]+\n", "\n", text)
    text = re.sub(r"\n[ ]+", "\n", text)
    return text.strip()


# =============================
# 2) 문장 후처리
# =============================
def postprocess_sentences(text: str, min_len=1, merge_len=25) -> str:
    text = re.sub(r"\s*\n+\s*", " ", text)
    text = re.sub(r"\s{2,}", " ", text).strip()

    parts = re.split(r"\s*\.\s*", text)

    result = []
    seen = set()

    for part in parts:
        sent = part.strip()
        if not sent or len(sent) < min_len:
            continue

        if len(sent) <= merge_len and result:
            result[-1] = f"{result[-1]} {sent}".strip()
            continue

        key = re.sub(r"\s+", " ", sent)
        if key in seen:
            continue

        seen.add(key)
        result.append(sent)

    return ".\n".join(result) + ("." if result else "")


# =============================
# 3) 번역 관련 함수
# =============================
def contains_korean(text: str) -> bool:
    return any("가" <= ch <= "힣" for ch in text)


def split_text(text: str, max_length=4000):
    chunks = []
    while len(text) > max_length:
        cut = text.rfind(" ", 0, max_length)
        if cut == -1:
            cut = max_length
        chunks.append(text[:cut])
        text = text[cut:]
    chunks.append(text)
    return chunks


def safe_translate(translator, text, src="ko", dest="en"):
    for attempt in range(3):
        try:
            return translator.translate(text, src=src, dest=dest).text
        except Exception as e:
            print(f"[ERROR] 번역 실패 ({attempt+1}/3): {e}")
            time.sleep(2)
    return ""


# =============================
# 4) 핵심 로직
# =============================
def merge_preprocess_translate(
    input_dir: str,
    output_file: str,
):
    input_path = Path(input_dir)
    txt_files = sorted(input_path.glob("*.txt"))

    if not txt_files:
        print("폴더에 txt 파일이 없습니다.")
        return

    print(f"텍스트 파일 {len(txt_files)}개 병합 시작")

    # 1️⃣ 모든 파일 병합
    merged_texts = []
    for file in txt_files:
        print(f"   - 병합 중: {file.name}")
        merged_texts.append(
            file.read_text(encoding="utf-8", errors="ignore")
        )

    merged_text = "\n".join(merged_texts)
    print(f"병합 후 길이: {len(merged_text)}자")

    # 2️⃣ 전처리
    cleaned = clean_text(merged_text)
    cleaned = postprocess_sentences(cleaned)
    print(f"전처리 후 길이: {len(cleaned)}자")

    # 3️⃣ 번역
    if not contains_korean(cleaned):
        print("한글 없음 → 번역 생략")
        final_text = cleaned
    else:
        translator = Translator()
        chunks = split_text(cleaned)
        translated_chunks = []

        for i, chunk in enumerate(chunks):
            print(f"번역 중... ({i+1}/{len(chunks)})")
            translated_chunks.append(safe_translate(translator, chunk))
            time.sleep(1)

        final_text = "\n".join(translated_chunks)

    # 4️⃣ 최종 결과 저장 (1개 파일)
    Path(output_file).write_text(final_text, encoding="utf-8")
    print("완료")
    print(f"저장 위치: {output_file}")
    print(f"최종 길이: {len(final_text)}자")


# =============================
# 실행부
# =============================
if __name__ == "__main__":
    merge_preprocess_translate(
        input_dir = r"C:\work\K리그_모음\DAEGU_FC", # 번역할 폴더
        output_file = r"C:\work\Project\sports-analysis-fighter\daegu_fc.txt", # 저장할 위치
    )