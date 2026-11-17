def lora_param_count(in_features, out_features, r):
    # [trained by LoRA, full layer (weight + bias)] counts
    return [0, 0]

print(lora_param_count(64, 64, 4))
print(lora_param_count(4096, 4096, 8))
