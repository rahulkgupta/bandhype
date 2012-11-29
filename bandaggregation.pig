register 'udfs.py' using jython as udfs;

tweet_original = LOAD 'fipsNov14Out500.txt' USING PigStorage('\t') AS (band, user, longitude, latitude, time, text, city, county, state, fips);
tweets = FOREACH tweet_original GENERATE band, udfs.get_day(time) as time, city, fips as county, SUBSTRING((chararray)fips,0,2) as state;


banded_state = GROUP tweets BY (state, band);
state_tweets = GROUP tweets BY state;
bs_count = FOREACH banded_state GENERATE FLATTEN($0), COUNT($1) as count;
s_count = FOREACH state_tweets GENERATE $0, COUNT($1) as count;
bs_pct = JOIN bs_count by $0, s_count by $0;

bs_final = FOREACH bs_pct GENERATE $1, $0, (float)$2/(float)$4;

STORE bs_final INTO 'novbscount.txt' USING PigStorage(',');