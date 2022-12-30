# SlippiRankDisplay

This is a program that displays and tracks information relating to your ranked Slippi profile.
Rank is not currently displayed (although rating is) because rank cannot be directly retrieved from Slippi's GraphQL database.
This is built with the intention of having minimal impact on Slippi resources to avoid inflating costs, so a full scrape of the website to retrieve rank is not planned.

### Usage

Use File -> Settings to enter your Slippi code. Invalid codes will result in default settings being used.

### Rank Tracking

A graph with saved ranked data is used to track an accounts rating over time. Note that a new point on the graph is only added when an account is updated
and points cannot be added after the fact. For this reason, it is best to open the program often (once after you have finished playing each day)
for the most accurate data tracking.

As mentioned above, this program is designed to have minimal impact on Slippi costs. Account data will only be updated once a day per code.
Every day at midnight local time, the current account will be updated. If you enter a code that has not been updated in the past day, it will be updated.

Account and graph data is saved to cache.json, so do not remove this or you will lose all data that has been tracked.

#Future Features

- Make sure the graph behaves correctly in all scenarios, the graph in general is very untested
- Add some sort of indication (sound, animation, etc.) when an accounts rating goes up or down
