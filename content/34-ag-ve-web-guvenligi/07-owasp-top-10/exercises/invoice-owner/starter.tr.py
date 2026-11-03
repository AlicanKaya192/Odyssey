def get_invoice(invoices, user, invoice_id):
    for invoice in invoices:
        if invoice["id"] == invoice_id:
            return invoice["amount"]
    return "not found"

INVOICES = [{"id": 101, "owner": "ada", "amount": 250},
            {"id": 102, "owner": "bob", "amount": 990}]
print(get_invoice(INVOICES, "ada", 101))
print(get_invoice(INVOICES, "ada", 102))
print(get_invoice(INVOICES, "ada", 999))
