import json
from classifier import classify_return

test_cases = [
    # Easy English cases
    {"input": "I want my money back, the stroller was broken", "expected": "refund"},
    {"input": "I'd like to exchange this for a different size", "expected": "exchange"},
    {"input": "I'm okay with store credit for the returned item", "expected": "store_credit"},
    {"input": "The product injured my baby, this is dangerous!", "expected": "escalate"},
    
    # Arabic cases
    {"input": "أريد استرداد أموالي، المنتج كان معيباً", "expected": "refund"},
    {"input": "أريد استبدال المنتج بمقاس مختلف", "expected": "exchange"},
    {"input": "يمكنني قبول رصيد المتجر بدلاً من الاسترداد", "expected": "store_credit"},
    {"input": "المنتج تسبب في أذى لطفلي، أحتاج مساعدة عاجلة", "expected": "escalate"},
    
    # Adversarial cases - model should return null
    {"input": "hello how are you", "expected": None},
    {"input": "what is the weather today", "expected": None},
    {"input": "I received the wrong item but I love it anyway", "expected": "exchange"},
]

def run_evals():
    print("Running Mumzworld Return Classifier Evals\n")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for i, case in enumerate(test_cases, 1):
        result = classify_return(case["input"])
        got = result.get("classification")
        expected = case["expected"]
        confidence = result.get("confidence", 0)
        
        status = "PASS" if got == expected else "FAIL"
        if status == "PASS":
            passed += 1
        else:
            failed += 1
        
        print(f"Test {i}: {status}")
        print(f"  Input:      {case['input'][:60]}")
        print(f"  Expected:   {expected}")
        print(f"  Got:        {got}")
        print(f"  Confidence: {int(confidence*100)}%")
        print()
    
    print("=" * 60)
    print(f"Results: {passed}/{len(test_cases)} passed ({int(passed/len(test_cases)*100)}%)")

if __name__ == "__main__":
    run_evals()