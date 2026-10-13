def rouge_l(candidate, reference):
    return 0.0

ref = "the parcel arrived damaged and the customer wants a refund"
print(rouge_l("the customer wants a refund", ref))
print(rouge_l("refund wants customer the", ref))
