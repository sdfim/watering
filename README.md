# watering

raspberry - router - (repiter) - esp(espeasy)


fill file - const_zones.json

include in crontab files:
00 22 * * * python3 /path/c_timer.php > /dev/null 2>&1
*/10 * * * * python3 /path/watering.php > /dev/null 2>&1


