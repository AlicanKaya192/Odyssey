def prediction_record(customer_id, score, version, threshold):
    decision = "offer" if score >= threshold else "no offer"
    return {"id": customer_id, "version": version,
            "score": round(score, 3), "decision": decision}


record = prediction_record("C06-00001", 0.42571, 3, 0.31)
print(record["id"], record["version"])
print(record["score"], record["decision"])
print(prediction_record("C06-00002", 0.1, 3, 0.31)["decision"])
