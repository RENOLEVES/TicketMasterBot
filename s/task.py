import subprocess
import time
from main import fetch_data
from process import process

start_time = time.time()

Keyshia_Cole = {
    "name":"Keyshia Cole",
    "url":r"https://www.ticketmaster.ca/keyshia-cole-the-way-it-is-toronto-ontario-07-09-2025/event/1000628EAB411C0B"
}

Sarah_McLachlan = {
    "name":"Sarah McLachlan",
    "url":r"https://www.ticketmaster.ca/sarah-mclachlan-fumbling-towards-ecstasy-30th-toronto-ontario-11-08-2025/event/1000628FAC742496"
}

Black_Pink = {
    "name":"BlackPink",
    "url":r"https://www.ticketmaster.ca/blackpink-2025-world-tour-toronto-ontario-07-22-2025/event/10006252DC87273D"
}

Chris_Brown = {
    "name":"Chris Brown",
    "url":r"https://www.ticketmaster.ca/chris-brown-breezy-bowl-xx-toronto-ontario-08-19-2025/event/1000627896EF168E"
}


# already happened.
# Taylor_Swift = {
#     "name":"Taylor Swift",
#     "url":r"https://www.ticketmaster.ca/the-story-of-taylor-swift-pickering-ontario-04-25-2025/event/100061859FC01609"
# }

pipeline = [
    Keyshia_Cole,
    Sarah_McLachlan,
    Black_Pink,
    Chris_Brown,
]

for task in pipeline:
    fetch_data(task.get("url"))
    time.sleep(1)
    process(task.get("name"))

end_time = time.time()
print("\nDone.")
print("seconds: ",end_time-start_time)