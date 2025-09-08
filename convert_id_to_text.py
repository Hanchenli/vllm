from vllm.transformers_utils.tokenizer import get_tokenizer

tokenizer = get_tokenizer("openai/gpt-oss-20b")

all_text = ""
with open("./token_id_log", "r") as f:
    for line in f:
        # Each line is like [222], so extract the number inside brackets
        token_id = int(line.strip().strip('[]'))
        text = tokenizer.decode([token_id])
        all_text += text
print(all_text)

# vllm engine.generate, feed in token such that <think> is not in the input
