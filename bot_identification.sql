-- assuming 
-- Twitter timestamp field named tweet_created
-- Twitter user ID field named user_id
-- Twitter coordinate fields named tweet_lat and tweet_lon

alter table london_tweets add column tw_cr_date date;
update london_tweets set tw_cr_date = date_trunc('day',tweet_created);
alter table london_tweets add column tw_u_loc_date integer;

with tw_u_loc_date_count as
(select count(*) as tw_count, user_id, tweet_lat, tweet_lon, tw_cr_date from london_tweets group by user_id, tweet_lat, tweet_lon, tw_cr_date)
update london_tweets as d set tw_u_loc_date = tw_count from tw_u_loc_date_count as s where d.user_id = s.user_id and d.tw_cr_date = s.tw_cr_date and d.tweet_lat = s.tweet_lat and d.tweet_lon = s.tweet_lon;

alter table london_tweets add column bot1 boolean;

with bots as
(select distinct(user_id) from london_tweets where tw_u_loc_date > 10)
update london_tweets as d set bot1 = true from bots as s where d.user_id = s.user_id;

alter table london_tweets add column bot1 boolean;

-- based on manual investigation:
alter table london_tweets add column bot2 boolean;
update london_tweets set bot2 = true where tweet_source like '"<a href=\\"http://www.tweetmyjobs.com\\" rel=\\"nofollow\\">TweetMyJOBS</a>"';
update london_tweets set bot2 = true where tweet_source like '"<a href=\\"https://dlvrit.com/\\" rel=\\"nofollow\\">dlvr.it</a>"';
update london_tweets set bot2 = true where tweet_source like '"<a href=\\"https://www.hootsuite.com\\" rel=\\"nofollow\\">Hootsuite Inc.</a>"';
update london_tweets set bot2 = true where tweet_source like '"<a href=\\"https://www.careerarc.com\\" rel=\\"nofollow\\">CareerArc 2.0</a>"';

update london_tweets set bot = true where bot1 is true or bot2 is true;

select count(*) from london_tweets where bot1 = true
