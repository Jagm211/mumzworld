import requests
import json

OPENROUTER_API_KEY = "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"
MODEL = "nvidia/nemotron-3-super-120b-a12b:free"

SYSTEM_PROMPT = """You are a return request classifier for Mumzworld, the largest mother and baby e-commerce platform in the Middle East.

Classify the customer return reason into exactly one of: refund, exchange, store_credit, escalate

Respond ONLY with valid JSON, no extra text:
{"classification": "refund", "confidence": 0.95, "reasoning_en": "customer wants money back", "reasoning_ar": "العميل يريد استرداد المال", "suggested_reply_en": "We will process your refund within 3-5 days.", "suggested_reply_ar": "سنعالج استردادك خلال 3-5 أيام."}

If input is not a return reason, use classification: null and confidence: 0.0"""

def classify_return(reason):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Classify this return reason: {reason}"}
        ],
        "temperature": 0.1
    }
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=body,
            timeout=30
        )
        response.raise_for_status()
        raw = response.json()["choices"][0]["message"]["content"]
        raw = raw.strip()
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start != -1 and end != 0:
            return json.loads(raw[start:end])
        return {"classification": None, "confidence": 0.0, "reasoning_en": "Could not parse response", "reasoning_ar": "تعذر تحليل الاستجابة", "suggested_reply_en": "Please contact support.", "suggested_reply_ar": "يرجى التواصل مع الدعم."}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    tests = [
        "I want my money back, the stroller was broken",
        "أريد استرداد أموالي، العربة كانت مكسورة",
        "I'd like to exchange for a different size",
        "hello how are you"
    ]
    for t in tests:
        print(f"\nInput: {t}")
        print(json.dumps(classify_return(t), ensure_ascii=False, indent=2))