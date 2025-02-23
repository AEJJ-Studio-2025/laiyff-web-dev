# laiyff-web-dev
A website for LA international youth film festival.

## How to start this website on our AWS server
```
1. ssh ${USER}@15.157.97.254
2. git clone git@github.com:AEJJ-Studio-2025/laiyff-web-dev.git
3. Got a database connected
4. cd laiyff-web-dev/utilScripts
5. ./initialEnv.sh # only run first time or requirements changed
4. ./makeMigrations.sh # only run when migration is needed
5. ./runWebsite.sh
```
