# watering

for use <br>
raspberry - router - (repiter) - one or more esp(espeasy) <br>
or only raspberry <br>
or raspberry and esp <br>

fill in the file - const_zones.json <br>
exampe <br>
{
"zones": [ <br>
    {"name": "z1", "gpio": "14", "norm": 3, "http_esp": "http://192.168.0.54:84"},  <br>
    {"name": "z2", "gpio": "12", "norm": 3, "http_esp": "http://192.168.0.54:84"}, <br>
    {"name": "z3", "gpio": "25", "norm": 2}, <br>
    {"name": "z4", "gpio": "27", "norm": 4}], <br>
"start_h_watering": 19 <br>
} <br>
if present key 'http_esp', then used gpio on esp, else used gpio raspberry pi (orange pi, etc) <br>
key 'norm' - norm waterin in mm/m2 <br>

add the following content to crontab: <br>
00 22 * * * python3 /your_path/c_timer.py > /dev/null 2>&1 <br>
*/15 * * * * python3 /your_path/watering.py > /dev/null 2>&1 <br>
