import json

signed_messages = json.load(open("../../../datasets/blockchain_info/signed_messages/blockchain_info_tags.json"))
submitted_links = json.load(open("../../../datasets/blockchain_info/submitted_links/blockchain_info_tags.json"))
assert len(set(signed_messages.keys()).intersection(set(submitted_links.keys()))) == 0, "Tags have addresses in common!"
tags = signed_messages.copy()
tags.update(submitted_links)
with open("../../../datasets/blockchain_info/tags.json", "wb") as file_handler:
    file_handler.write(json.dumps(tags))
print("Tags merged into file 'datasets/blockchain_info/tags.json'")
