import argparse
import os
import requests
import json
import datetime

parser = argparse.ArgumentParser(description="Bulk downloads up to 200 of the specified user's pgn files from Lichess.org")
parser.add_argument("username", help="Lichess.org username")
parser.add_argument("num", type=int, nargs="?", default=200, help="Number of pgn files to fetch (most recent first). Defaults to 200")
args = parser.parse_args()

target_dir = "lichess_pgns/" + args.username + "/"

if not os.path.exists(target_dir):
    os.makedirs(target_dir)

games_url = "https://en.lichess.org/api/user/" + args.username + "/games?nb=" + str(args.num) + "&with_moves=1"
pgn_url = "https://en.lichess.org/game/export/"
data = requests.get(games_url).text
data = json.loads(data)
filenames = {}
dir_contents = os.listdir(target_dir)
count = 0

for game in data["currentPageResults"]:
    timestamp = datetime.datetime.utcfromtimestamp((int(game["createdAt"]))/1000.0)
    date = timestamp.strftime("%d_%b_%y")
    filenames[game["id"]] = (game["players"]["white"]["userId"] + "_vs_" + game["players"]["black"]["userId"] + "_" + date + "_" + game["id"] + ".pgn")

print(filenames)

for filename in filenames:
    if filenames[filename] not in dir_contents:
        path = target_dir + filenames[filename]
        pgn = requests.get(pgn_url + filename + ".pgn").text
        print(pgn_url + filename)
        print("writing " + filenames[filename])
        with open(path, "w+") as f:
            f.write(pgn)
        count = count + 1
print("\nFetched " + str(count) + " files")
