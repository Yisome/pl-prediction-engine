Hey there

Quick Introduction: This project was a for fun project for me to learn how to fetch data, model it, use it, and display it.

Did it for a premier league match predictor because I love watching soccer and this is how I would love to learn how to code, doing it in conjuction with the things I love to do.

I'll make a what I learned statement at the end...

I already included a lot of comments but I'll run down the scripts

fetch_data.py:

Mainly just learned how to fetch the data and transform it into a database. Essentially retrieved data from the API-Football API using the correct endpoint and parameter to fetch the data of the 2023 PL season

Then, I just went through each fixture of that season and got the nitty gritty basic details of each match using a dictionary and appending it to an array.
Made a dataframe for that array and converted it to a sqlite database

8/24/25

Ran into a problem; football-api only lets me use so many requests a day which is pretty bad considering the accessing and looping of the get_stats function is now limited by the free tier of the api so I decided to download the Kaggle Premier League 2000-2023 historical data set and change the fetch_data.py.

I will still use the football-api for live matches though, I shall see.

