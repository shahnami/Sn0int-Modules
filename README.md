# Sn0int

## Usage
* `./start.sh <port> <workspace> <output> <interactive>`
	
#### Interactive Mode
* `./start.sh 9008 google output true`

#### Docker Mode
* `./start.sh 9008 google output false`
	
## Modules

### Importer

Make sure to have the following `targets.txt` file in the `/jobs` folder.

1. `./start.sh 9008 google output true`
2. `[sn0int][google] > use import`
3. `[sn0int][google][shahnami/import] > run`

### Exporter

1. `./start.sh 9008 google output true`
2. `[sn0int][google] > use export`
3. `[sn0int][google][shahnami/export] > set host localhost`
4. `[sn0int][google][shahnami/export] > set port 9008`
5. `[sn0int][google][shahnami/export] > set command json`
6. `[sn0int][google][shahnami/export] > run`

