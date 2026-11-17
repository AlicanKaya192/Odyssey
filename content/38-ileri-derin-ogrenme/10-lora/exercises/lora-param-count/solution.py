def lora_param_count(in_features, out_features, r):
    lora = r * (in_features + out_features)
    full = in_features * out_features + out_features
    return [lora, full]

print(lora_param_count(64, 64, 4))
print(lora_param_count(4096, 4096, 8))
