# watering

raspberry - router - (repiter) - one or more esp(espeasy) <br>


fill file - const_zones.json <br>

include in crontab files: <br>
00 22 * * * python3 /your_path/c_timer.py > /dev/null 2>&1 <br>
*/10 * * * * python3 /your_path/watering.py > /dev/null 2>&1 <br>
