## Local Television Area

"A media market, broadcast market, media region, designated market area (DMA), television market area, or simply market is a region where the population can receive the same (or similar) television and radio station offerings." --- [https://en.wikipedia.org/wiki/Media_market](Wikipedia)

In the Internet era, with an ever increasing proportion of households that have 'cut-the-cord,' media markets mean less than ever. But local television news continues to draw older people. And local network affiliates are still an important part of media 'diets' of older Americans. 

Using [FCC DTV Maps](https://www.fcc.gov/media/engineering/dtvmaps), we first create a comprehensive database of all local channels per zip code. Then, we cluster zip codes using k-means, choosing k in a way that follows the 'elbow' rule. We also produce a clustering with the constraint that zip codes can only be merged with other zip codes in the 'same' county (over 90% share).

### Workflow

We use the list of [zip codes](data/us_zipcodes.csv) and iterate over [FCC DTV Maps](https://www.fcc.gov/media/engineering/dtvmaps) and produce a CSV with the following columns:

(each zipcode will have multiple rows --- one row per channel)

`zipcode, callsign, network, channel_number, band, ia, signal_strength (strong/moderate, weak, no signal), facility_id, city_of_license, rf_channel, rx_strength, tower_distance, repacked_channel, repacking_dates`

![example](example.png)

