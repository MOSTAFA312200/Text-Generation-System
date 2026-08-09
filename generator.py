from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM

from config import (
    MODEL_NAME,
    MAX_NEW_TOKENS,
    TEMPERATURE,
    TOP_K,
    TOP_P,
)


def validate_config():
    if MAX_NEW_TOKENS <= 0:
        raise ValueError(
            "MAX_NEW_TOKENS must be greater than 0."
        )

    if TEMPERATURE <= 0:
        raise ValueError(
            "TEMPERATURE must be greater than 0."
        )

    if TOP_K < 0:
        raise ValueError(
            "TOP_K cannot be negative."
        )

    if not 0 < TOP_P <= 1:
        raise ValueError(
            "TOP_P must be between 0 and 1."
        )


validate_config()


tokenizer = None
model = None


def load_model():
    global tokenizer, model

    if tokenizer is None or model is None:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)


def generate_text(prompt):
    load_model()

    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=MAX_NEW_TOKENS,
        do_sample=True,
        temperature=TEMPERATURE,
        top_k=TOP_K,
        top_p=TOP_P,
    )

    text = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return text