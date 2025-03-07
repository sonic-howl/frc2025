docker run -d --network=host --name=grafana   --volume grafana-storage:/var/lib/grafana   grafana/grafana
docker run --network=host -d -v influxdb:/var/lib/influxdb --name influx influxdb:1.8
telegraf --config telegraf.conf
