DEXY
===============

Dex tool capable of making ETH accounts and doing transactions across multiple DEX's in order to trade via their API's and/or obtain future airdrops.

Requirements
===============

* python3.9
* infra.io `project_id` and `project_secret`
* requirements.txt

Installation
===============

```bash

python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt

```

Run
===============
```bash
export ACCOUNT_RANDOMNESS='' INFURA_PROJECT_ID='' INFURA_PROJECT_ID=''
python3 dexy.py -e {environment} -d {dex} -c {connection_type}
```
