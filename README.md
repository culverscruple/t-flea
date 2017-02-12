# silver-guacamole
Bulk download .pgn files from Lichess.org

Usage:
`python3 fetch_pgns.py <username> <number>`

To automatically download any new pgns once a day, create a script with the following contents and place in /etc/cron.daily:

```
#!/bin/bash

python3 /path/to/fetch_pgns.py <username> -d /target/directory
```
