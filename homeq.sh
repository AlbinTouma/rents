URL="https://api.homeq.se/api/v3/search"
DATE=$(date +%F)
OUTPUT_DIR="data"
PAGE=1
PAYLOAD=$(cat <<EOF
{
"sorting":"boost_value.desc","geo_bounds":{"min_lat":57.64099754479133,"min_lng":11.931791837032364,"max_lat":57.713389380914094,"max_lng":12.003244081129196},"zoom":10,"page":$PAGE,"amount":40
}
EOF
)

curl $URL \
-H 'accept: */*'   -H 'accept-language: en-GB,en;q=0.9,en-US;q=0.8,sv;q=0.7,ro;q=0.6'   -H 'cache-control: no-cache'   -H 'content-type: application/json'   -H 'origin: https://www.homeq.se'   -H 'pragma: no-cache'   -H 'priority: u=1, i'   -H 'referer: https://www.homeq.se/'   -H 'sec-ch-ua: "Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"'   -H 'sec-ch-ua-mobile: ?1'   -H 'sec-ch-ua-platform: "Android"'   -H 'sec-fetch-dest: empty'   -H 'sec-fetch-mode: cors'   -H 'sec-fetch-site: same-site'   -H 'user-agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36' \
--data-raw "$PAYLOAD" |\
jq '.results[] | {id: .id, city: .city, county: .county, location: .location, uri: .uri, title: .title, rent: .rent, rooms: .rooms, area: .area, rent: .rent, date_access: .date_access, references: .references} ' >> $OUTPUT_DIR/homeq_$DATE.json
