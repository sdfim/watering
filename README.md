# watering

raspberry - router - (repiter) - one or more esp(espeasy) <br>


fill file - const_zones.json <br>

include in crontab files: <br>
00 22 * * * python3 /path/c_timer.php > /dev/null 2>&1 <br>
*/10 * * * * python3 /path/watering.php > /dev/null 2>&1 <br>


