"""Help-centre articles of a fictional outdoor shop, for the retrieval exercises (read-only).

DOCS: the articles. QUESTIONS: questions with the article that answers them
("doc") and a short phrase a correct answer must contain ("key"); the last
three have no answer in the articles (doc and key are None).
"""

DOCS = [
    {"id": "shipping", "title": "Shipping costs and delivery times",
     "text": "Orders over 50 euros ship for free. Smaller orders pay a shipping fee of 4.90 euros. "
             "Standard delivery takes 3 to 5 working days. Express delivery costs 9.90 euros and arrives "
             "on the next working day if you order before 14:00. We ship to all EU countries, Norway and "
             "Switzerland. We do not ship outside Europe."},
    {"id": "returns", "title": "Returning an item",
     "text": "You can return items within 30 days of delivery. Items must be unused and still have their "
             "tags. The return label is free inside the EU. Outlet items are final sale and cannot be "
             "returned. Boots that have been worn outdoors cannot be returned, so please try them on "
             "indoors first."},
    {"id": "refunds", "title": "Refunds",
     "text": "We pay your refund to the original payment method within 7 days after the warehouse receives "
             "your return. Purchases paid with a gift card are refunded as a new gift card. Shipping costs "
             "are refunded only if you return the whole order."},
    {"id": "warranty", "title": "Warranty",
     "text": "All products have a warranty of 2 years. Tents and backpacks have a warranty of 5 years on "
             "seams and zippers. The warranty does not cover normal wear and tear or damage from misuse. "
             "To make a claim, send a photo of the damage and your order number."},
    {"id": "payment", "title": "Payment methods",
     "text": "You can pay by credit card, debit card or bank transfer. Business customers can also pay by "
             "invoice. Orders over 300 euros can be paid in 3 monthly instalments without extra cost."},
    {"id": "giftcards", "title": "Gift cards and discount codes",
     "text": "Gift cards are available for 25, 50 and 100 euros and are valid for 3 years. They cannot be "
             "exchanged for cash. You can use one gift card and one discount code per order."},
    {"id": "account", "title": "Your account and password",
     "text": "A password reset link is valid for 24 hours. After 5 failed login attempts your account is "
             "locked for 15 minutes. You can delete your account in the settings; your data is removed "
             "within 30 days."},
    {"id": "loyalty", "title": "Loyalty points",
     "text": "You earn 1 point for every euro you spend. 100 points give you a voucher of 5 euros. Points "
             "expire if you make no purchase for 12 months. Members get early access to our sales."},
    {"id": "tents", "title": "Caring for your tent",
     "text": "Always dry your tent completely before storing it, otherwise mould can grow on the fabric. "
             "Clean it with lukewarm water and no detergent. Seal the seams again every 2 seasons. Store the "
             "tent loosely, not tightly packed."},
    {"id": "boots", "title": "Caring for your boots",
     "text": "Break in new boots over 2 weeks with short walks. Brush off dried mud after every hike. With "
             "regular use, waterproof the boots again every 3 months. Dry them away from heaters, because "
             "heat makes the leather crack."},
    {"id": "sleeping", "title": "Sleeping bags",
     "text": "The comfort temperature is the lowest temperature at which an average sleeper stays warm. The "
             "limit temperature is lower and only means you will not get dangerously cold. Store sleeping "
             "bags uncompressed in the large storage sack. Wash down sleeping bags at most twice a year at "
             "30 degrees with a special down detergent."},
    {"id": "service", "title": "Customer service and store hours",
     "text": "Customer service is open Monday to Friday, 9:00 to 17:00, by phone and chat. We answer emails "
             "within 2 working days. Our store is open Monday to Saturday, 10:00 to 19:00, and closed on "
             "Sundays and public holidays."},
    {"id": "international", "title": "Orders to Norway and Switzerland",
     "text": "For orders to Norway and Switzerland the customer pays the customs fees. Delivery takes 5 to 8 "
             "working days. Returns from these countries are not free; the customer pays the return "
             "shipping."},
    {"id": "repairs", "title": "Repair service",
     "text": "We repair broken zips for free while the product is under warranty. After the warranty, a "
             "repair costs from 15 euros. A repair usually takes 3 weeks."},
]

QUESTIONS = [
    {"q": "How much does shipping cost for a 30 euro order?", "doc": "shipping", "key": "4.90"},
    {"q": "When will my express order arrive if I order at noon?", "doc": "shipping", "key": "next working day"},
    {"q": "Can I return boots I wore on a hike?", "doc": "returns", "key": "cannot be returned"},
    {"q": "How long do I have to send something back?", "doc": "returns", "key": "30 days"},
    {"q": "When will I get my money back?", "doc": "refunds", "key": "7 days"},
    {"q": "I paid with a gift card, how is my refund paid?", "doc": "refunds", "key": "new gift card"},
    {"q": "How long is the warranty on a tent zipper?", "doc": "warranty", "key": "5 years"},
    {"q": "Can I pay in instalments?", "doc": "payment", "key": "3 monthly instalments"},
    {"q": "Do gift cards expire?", "doc": "giftcards", "key": "3 years"},
    {"q": "My reset link does not work anymore.", "doc": "account", "key": "24 hours"},
    {"q": "How many points do I need for a voucher?", "doc": "loyalty", "key": "100 points"},
    {"q": "How do I stop mould in my tent?", "doc": "tents", "key": "dry your tent"},
    {"q": "How often should I waterproof my boots?", "doc": "boots", "key": "3 months"},
    {"q": "Can I wash my down sleeping bag?", "doc": "sleeping", "key": "twice a year"},
    {"q": "When can I call customer service?", "doc": "service", "key": "9:00 to 17:00"},
    {"q": "Is the store open on Sunday?", "doc": "service", "key": "closed on Sundays"},
    {"q": "Do I pay customs when ordering to Switzerland?", "doc": "international", "key": "customs fees"},
    {"q": "How much does it cost to fix a broken zip after the warranty?", "doc": "repairs", "key": "15 euros"},
    {"q": "How long does a repair take?", "doc": "repairs", "key": "3 weeks"},
    {"q": "Why is my account locked?", "doc": "account", "key": "5 failed login attempts"},
    {"q": "Do my points expire?", "doc": "loyalty", "key": "12 months"},
    {"q": "Can I use two discount codes?", "doc": "giftcards", "key": "one discount code"},
    {"q": "Do you deliver to Canada?", "doc": "shipping", "key": "outside Europe"},
    {"q": "What does the comfort temperature of a sleeping bag mean?", "doc": "sleeping", "key": "stays warm"},
    {"q": "Do you sell bicycles?", "doc": None, "key": None},
    {"q": "In which year was the shop founded?", "doc": None, "key": None},
    {"q": "Can I pick up my order in the store?", "doc": None, "key": None},
]
