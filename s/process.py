import datetime
import os.path
from lxml import html
from utils import expand_custom
import pandas as pd
import re
import json

seat_df = pd.DataFrame(columns=["data-price", "description", "section", "row", "branding", "place"])
place_df = pd.DataFrame(columns=["section", "place", "offerId"])
price_df = pd.DataFrame(columns=["offerId", "name", "totalPrice"])

with open("../data1.html", "r", encoding="utf-8") as file:
    content = file.read()

tree = html.fromstring(content)
current_date = datetime.date.today()

with open("../facets.json", "r") as file:
    data = json.load(file)

# seat df
facets = data['facets']

for (i, facet) in enumerate(facets, 1):

    offers = facet["offers"]
    section_name = facet["section"]

    places = []
    for place in facet["places"]:
        places.extend(expand_custom(place))
    if not places:
        places = None

    place_df.loc[i] = [section_name, places, offers]

with open("../offer.json", "r") as file:
    data = json.load(file)

# price df
offers = data["_embedded"]["offer"]

for (i, offer) in enumerate(offers, 1):
    offerId = offer["offerId"]
    name = offer.get("name", offer.get("inventoryType"))

    totalPrice = offer["totalPrice"]

    price_df.loc[i] = [offerId, name, totalPrice]

# Use XPath to find the <li> elements
items = tree.xpath('//li[@role="menuitem" and @aria-haspopup="dialog"]')

svg_blocks = tree.xpath('//*[local-name()="g" and @data-component="svg__block"]')
i = 1
for block in svg_blocks:
    section_name = block.get("data-section-name")
    svg_rows = block.xpath('.//*[local-name()="g" and @data-component="svg__row"]')
    for row in svg_rows:
        row_name = row.get("data-row-name")
        svg_seats = row.xpath('.//*[ (local-name()="circle" and @data-component="svg__seat") or (local-name()="g" and '
                              '@data-component="svg__seat")]')
        for seat in svg_seats:
            seat_name = seat.get("data-seat-name")
            place = seat.get("id")
            p = seat.get("class")
            if "is-resale" in p:
                branding = "Verified Resale Ticket"
            elif "is-locked" in p:
                branding = "Standard Admission/Unlock"
            elif "is-vip-star" in p:
                branding = "VIP Package"
            elif "is-ada" in p:
                branding = "Standard Admission/Wheelchair Accessible"
            elif "is-available" in p:
                branding = "Standard Admission"
            else:
                branding = "Not available"

            seat_df.loc[i] = [0, f"Sec {section_name} • Row {row_name} • Seat {seat_name}", section_name, row_name,
                              branding, place]
            i = i + 1

title = tree.xpath('//title[normalize-space()]')[0].text

# artist_name = re.match("(.*?):", title).group(1)
artist_name = "BlackPink"

if not os.path.isdir(f"../data/price/{artist_name}"):
    os.makedirs(f"../data/price/{artist_name}")

if not os.path.isdir(f"../data/seat/{artist_name}"):
    os.makedirs(f"../data/seat/{artist_name}")

if not os.path.isdir(f"../data/place/{artist_name}"):
    os.makedirs(f"../data/place/{artist_name}")

if not os.path.isdir(f"../data/result/{artist_name}"):
    os.makedirs(f"../data/result/{artist_name}")

seat_df.to_excel(f"../data/seat/{artist_name}/{current_date}.xlsx", index=False)
price_df.to_excel(f"../data/price/{artist_name}/{current_date}.xlsx", index=False)
place_df.to_excel(f"../data/place/{artist_name}/{current_date}.xlsx", index=False)

place_df.dropna(subset="place", inplace=True)

place_df["offerId"] = place_df["offerId"].apply(
    lambda x: x[0] if isinstance(x, list) else x
)
mapping = price_df.set_index("offerId")["totalPrice"].to_dict()

place_df["data-price"] = place_df["offerId"].map(mapping)

exploded_place_df = place_df.explode("place")

# Now create the mapping from offerId to totalPrice
price_mapping = exploded_place_df.set_index("place")["data-price"].to_dict()

seat_df["data-price"] = seat_df["place"].map(price_mapping)

seat_df = seat_df[["data-price", "description", "branding"]]

seat_df.to_excel(f"data/result/{artist_name}/{current_date}.xlsx", index=False)
#

#
# price_df.to_excel(f"data/price/{artist_name}/{current_date}.xlsx", index=False)
#
# with pd.ExcelWriter(f"data/seat/{artist_name}/{current_date}.xlsx", "xlsxwriter") as writer:
#     workbook = writer.book
#     worksheet = workbook.add_worksheet()
#     writer.sheets["sheet1"] = worksheet
#
#     seat_df.to_excel(writer,startrow=1, index=False)
#
#
# del seat_df["data-price"]
#
# price_df.loc[price_df['branding'].str.contains("Standard Ticket"),"branding"] = "Standard Admission"
#
# price_df = price_df.dropna(subset=['row','section'])
#
# print("price_df", price_df.head(5))
# price_df.drop(columns=['description'], inplace=True)
#
# result = pd.merge(seat_df, price_df, on=['section', 'row', 'branding'], how='left')
#
# result = pd.merge(result, price_df[['section', 'row', 'data-price']],
#                   on=['section', 'row'],
#                   how='left',
#                   suffixes=('', '_df2'))
#
# result.loc[(result['branding'] == 'Standard Admission') &
#            (result['data-price'].isna()), 'data-price'] = result['data-price_df2']
#
# result = result[['data-price', 'description', 'branding']]
# result.to_excel(f"data/result/{artist_name}/{current_date}.xlsx", index=False)
