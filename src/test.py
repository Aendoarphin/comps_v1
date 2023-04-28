from ebay.ebay import Ebay

payload = {
    "keywords" : "jamahal hill panini prizm red refractor",
    "excluded_keywords":"box case break",
    "max_search_results":"240",
    "category_id":"26328",
    "remove_outliers":True,
    "site_id":"0",
    "aspects":[{"name": "Graded", "value": "No"}]
}

# FOR TESTING
def print_dict(data):
    # Get the first two items from the dictionary
    first_two_items = dict(list(data.items())[:3])
    # Iterate through the first two items in the dictionary and print each one
    for key, value in first_two_items.items():
        print(f"{key}: {value}")

ebay = Ebay()

# SAMPLE INPUT
# print_dict(
#     ebay.make_request(payload)
# )

print(ebay.make_request(payload))

