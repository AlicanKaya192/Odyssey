def lora_params(d_in, d_out, r):
    return [0, 0, 0.0]


print(lora_params(64, 32, 4))
print(lora_params(4096, 4096, 8))
