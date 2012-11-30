register 'udfs.py' using jython as udfs;

tweet_original = LOAD 'fipsNov14Out500.txt' USING PigStorage('\t') AS (band, user, longitude, latitude, time, text, city, county, state, fips);
tweets = FOREACH tweet_original GENERATE band, udfs.get_day(time) as time, city, fips as county, SUBSTRING((chararray)fips,0,2) as state;


banded_state = GROUP tweets BY (state, band);
state_tweets = GROUP tweets BY state;
bs_count = FOREACH banded_state GENERATE FLATTEN($0), COUNT($1) as count;
s_count = FOREACH state_tweets GENERATE $0, COUNT($1) as count;
bs_pct = JOIN bs_count by $0, s_count by $0;

bs_final = FOREACH bs_pct GENERATE $1, $0, (float)$2/(float)$4;

STORE bs_final INTO 'novbscount' USING PigStorage(',');

banded_county = GROUP tweets BY (county, band);
county_tweets = GROUP tweets BY county;
bc_count = FOREACH banded_county GENERATE FLATTEN($0), COUNT($1) as count;
c_count = FOREACH county_tweets GENERATE $0, COUNT($1) as count;
bc_pct = JOIN bc_count by $0, c_count by $0;

bc_final = FOREACH bc_pct GENERATE $1, $0, (float)$2/(float)$4;

STORE bc_final INTO 'novbccount' USING PigStorage(',');

banded_city = GROUP tweets BY (city, state, band);
city_tweets = GROUP tweets BY (city, state);
bcity_count = FOREACH banded_city GENERATE FLATTEN($0), COUNT($1) as count;
city_count = FOREACH city_tweets GENERATE FLATTEN($0), COUNT($1) as count;
bcity_pct = JOIN bcity_count by ($0, $1), city_count by ($0, $1);

bcity_final = FOREACH bcity_pct GENERATE $2, $0, $1, (float)$3/(float)$6;

STORE bcity_pct INTO 'novbcitycount' USING PigStorage(',');

bts = GROUP tweets BY (time, state, band);
ts = GROUP tweets BY (time, state);
bts_c = FOREACH bts GENERATE FLATTEN($0), COUNT($1) as count;
ts_c = FOREACH ts GENERATE FLATTEN($0), COUNT($1) as count;
bts_j = JOIN bts_c by ($0, $1), ts_c by ($0, $1);
bts_f = FOREACH bts_j GENERATE $2, $0, $1, (float)$3/(float)$6;

STORE bts_f INTO 'bts_f' USING PigStorage(',');

btc = GROUP tweets BY (time, county, band);
tc = GROUP tweets BY (time, county);
btc_c = FOREACH btc GENERATE FLATTEN($0), COUNT($1) as count;
ts_c = FOREACH tc GENERATE FLATTEN($0), COUNT($1) as count;
btc_j = JOIN btc_c by ($0, $1), ts_c by ($0, $1);
btc_f = FOREACH btc_j GENERATE $2, $0, $1, (float)$3/(float)$6;

STORE btc_f INTO 'btc_f' USING PigStorage(',');


btcy = GROUP tweets BY (time, city, state, band);
tcy = GROUP tweets BY (time, city, state);
btcy_c = FOREACH btcy GENERATE FLATTEN($0), COUNT($1) as count;
ts_c = FOREACH tcy GENERATE FLATTEN($0), COUNT($1) as count;
btcy_j = JOIN btcy_c by ($0, $1, $2), ts_c by ($0, $1, $2);
btcy_f = FOREACH btcy_j GENERATE $3, $0, $1, $2, (float)$4/(float)$8;

STORE btcy_f INTO 'btcy_f' USING PigStorage(',');



