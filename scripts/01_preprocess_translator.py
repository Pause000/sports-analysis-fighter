import re
import time
import os
import random
from pathlib import Path
# Python 3.13 호환성을 위해 deep-translator 사용 (pip install deep-translator 필요)
from deep_translator import GoogleTranslator

# =============================
# 1) 기존 전처리 함수 (유지)
# =============================
def clean_text(text: str) -> str:
    text = text.replace("\ufeff", "")
    text = text.replace("\u200b", "")
    text = re.sub(r"http[s]?://\S+", " ", text)
    text = re.sub(r"[\r\t]", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.replace("!", " ").replace("?", " ")
    text = re.sub(r"[^0-9A-Za-z가-힣\s\.\n]", " ", text)
    text = re.sub(r"[ ]{2,}", " ", text)
    return text.strip()

# =============================
# 2) 기존 후처리 로직 (유지: 문장별 .\n 구분)
# =============================
def postprocess_sentences(text: str, min_len=1, merge_len=25) -> list:
    # 💡 나중에 번역하기 편하도록 리스트 형태로 반환하게 살짝 수정했습니다.
    text = re.sub(r"\s*\n+\s*", " ", text)
    text = re.sub(r"\s{2,}", " ", text).strip()
    parts = re.split(r"\s*\.\s*", text)
    
    result = []
    seen = set()
    for part in parts:
        sent = part.strip()
        if not sent or len(sent) < min_len: continue
        if len(sent) <= merge_len and result:
            result[-1] = f"{result[-1]} {sent}".strip()
            continue
        key = re.sub(r"\s+", " ", sent)
        if key in seen: continue
        seen.add(key)
        result.append(sent)
    return result # 문장 리스트 반환

# =============================
# 3) 번역 함수 (deep-translator로 안정화)
# =============================
def safe_translate(text, src="ko", dest="en"):
    if not any("가" <= ch <= "힣" for ch in text): return text
    for attempt in range(3):
        try:
            # 문장 단위 번역으로 구조 붕괴 방지
            return GoogleTranslator(source=src, target=dest).translate(text)
        except Exception as e:
            print(f"      ⚠️ 번역 재시도 ({attempt+1}/3): {e}")
            time.sleep(random.uniform(1, 2))
    return text

# =============================
# 4) 핵심 로직
# =============================
def merge_preprocess_translate(input_dir: str, output_path: str):
    input_path_obj = Path(input_dir).resolve()
    output_path_obj = Path(output_path).resolve()
    txt_files = sorted(input_path_obj.glob("*.txt"))

    if not txt_files:
        print(f"❌ 파일을 찾을 수 없습니다: {input_path_obj}")
        return

    os.makedirs(output_path_obj, exist_ok=True)
    print(f"🚀 {len(txt_files)}개 파일 처리 시작 (전처리 로직 보존 모드)")

    for idx, file in enumerate(txt_files):
        print(f"▶ [{idx+1}/{len(txt_files)}] {file.name} 처리 중...")
        content = file.read_text(encoding="utf-8", errors="ignore")
        
        # 1. 원본 전처리 적용
        cleaned_text = clean_text(content)
        sentence_list = postprocess_sentences(cleaned_text) # 문장 리스트 획득
        
        # 2. 문장별 번역 (줄바꿈 보존의 핵심)
        translated_sentences = []
        for i, sent in enumerate(sentence_list):
            # 진행률 표시
            print(f"   ㄴ 번역 중: {i+1}/{len(sentence_list)}", end="\r")
            trans_sent = safe_translate(sent)
            translated_sentences.append(trans_sent)
            
        # 3. 기존 방식대로 .\n 으로 합치기
        final_text = ".\n".join(translated_sentences) + ("." if translated_sentences else "")

        # 4. 저장
        save_target = output_path_obj / f"{file.stem}_translated.txt"
        save_target.write_text(final_text, encoding="utf-8")
        print(f"\n   💾 저장 완료: {save_target.name}")

if __name__ == "__main__":
    merge_preprocess_translate(
        input_dir=r"", 
        output_path=r""
    )