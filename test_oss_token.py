from vllm.transformers_utils.tokenizer import get_tokenizer

tokenizer = get_tokenizer("openai/gpt-oss-20b")

id1 = tokenizer.encode("<|start|>")
print(id1)

id2 = tokenizer.encode("<|end|>")
print(id2)

id3 = tokenizer.encode("<|message|>")
print(id3)

id4 = tokenizer.encode("<|channel|>analysis<|end|>")
print(id4)


