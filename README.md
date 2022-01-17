## Local Television Area

"A media market, broadcast market, media region, designated market area (DMA), television market area, or simply market is a region where the population can receive the same (or similar) television and radio station offerings." --- [Wikipedia](https://en.wikipedia.org/wiki/Media_market)

In the Internet era, with an ever increasing proportion of households that have 'cut-the-cord,' media markets mean less than ever. But local television news continues to draw older people. And local network affiliates are still an important part of media 'diets' of older Americans. 

Using [FCC DTV Maps](https://www.fcc.gov/media/engineering/dtvmaps), we first create a comprehensive database of all local channels per zip code. Then, we cluster zip codes using k-means, choosing k in a way that follows the 'elbow' rule. We also produce a clustering with the constraint that zip codes can only be merged with other zip codes in the 'same' county (over 90% share).

### Scraping

We use the list of [zip codes](data/us_zipcodes.csv) and iterate over [FCC DTV Maps](https://www.fcc.gov/media/engineering/dtvmaps) and produce [a CSV](output/stations.csv) with the following columns:

(each zipcode has multiple rows --- one row per channel)

`zipcode, callsign, network, channel_number, band, ia, signal_strength (strong/moderate, weak, no signal), facility_id, city_of_license, rf_channel, rx_strength, tower_distance, repacked_channel, repacking_dates`

![example](example.png)

For ~ 2,000 zip codes, the search came back empty. Here's the [log file](output/log.zip).

**Scripts**

1. [Scrape](scripts/01_get_data.py)
2. [Generate CSV from Logs](scripts/02_generate_csv_from_logs.py)
3. [Checks](scripts/03_generate_metatdata.py)

### Clustering

1. [group_zips](scripts/cluster_manhattan_distance_optimized.ipynb): clusters zip codes based on overlap between list of TV stations (with certain signal strength) and appends the grouping variable. We use deterministic (within a certain manhattan distance) multi-assignment (each zipcode can be part of multiple clusters) clustering. We run it for diff = 0, 1, and 2 and save outputs in [output_diff_0.csv (zipped)](output/output_diff_0.zip), [output_diff_1.csv (zipped)](output/output_diff_1.zip) and [output_diff_2.csv (zipped)](output/output_diff_2.zip) respectively.

2. [k_means](scripts/05_k_means.ipynb): we use k-means to cluster zip codes based on overlap between list of TV stations (with certain signal strength) and appends the grouping variable. We run it for k = 200 and [save the output in (k_means_200.csv (zipped)](output/k_means_200.zip).

### Authors

Suriyan Laohaprapanon and Gaurav Sood
