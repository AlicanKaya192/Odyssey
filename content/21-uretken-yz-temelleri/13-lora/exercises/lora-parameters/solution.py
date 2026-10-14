def lora_params(d_in, d_out, r):
    full = d_in * d_out
    lora = r * (d_in + d_out)
    return [full, lora, round(lora / full, 4)]


print(lora_params(64, 32, 4))
print(lora_params(4096, 4096, 8))
