## Two Line Element

セッションの cookie を取得

```
$ curl -c cookies.txt -b cookies.txt -k https://www.space-track.org/ajaxauth/login -d "identity=myusername&password=mypassword"
```

cookie を用いてクエリを叩く

```
$ curl --limit-rate 100K --cookie cookies.txt "https://www.space-track.org/basicspacedata/query/class/tle_latest/ORDINAL/1/NORAD_CAT_ID/123/orderby/TLE_LINE1 ASC/format/tle" > sample.json
```

結果：

```
[
{
"ORDINAL": "1",
"COMMENT": "GENERATED VIA SPACETRACK.ORG API",
"ORIGINATOR": "JSPOC",
"NORAD_CAT_ID": "123",
"OBJECT_NAME": "THOR ABLESTAR DEB",
"OBJECT_TYPE": "DEBRIS",
"CLASSIFICATION_TYPE": "U",
"INTLDES": "61015H",
"EPOCH": "2016-04-17 12:16:35",
"EPOCH_MICROSECONDS": "580288",
"MEAN_MOTION": "14.36592551",
"ECCENTRICITY": "0.0108466",
"INCLINATION": "66.6852",
"RA_OF_ASC_NODE": "193.3195",
"ARG_OF_PERICENTER": "100.8307",
"MEAN_ANOMALY": "260.5024",
"EPHEMERIS_TYPE": "0",
"ELEMENT_SET_NO": "999",
"REV_AT_EPOCH": "84628",
"BSTAR": "9.4336e-05",
"MEAN_MOTION_DOT": "2.06e-06",
"MEAN_MOTION_DDOT": "0",
"FILE": "2022043",
"TLE_LINE0": "0 THOR ABLESTAR DEB",
"TLE_LINE1": "1 00123U 61015H   16108.51152292  .00000206  00000-0  94336-4 0  9999",
"TLE_LINE2": "2 00123  66.6852 193.3195 0108466 100.8307 260.5024 14.36592551846284",
"OBJECT_ID": "1961-015H",
"OBJECT_NUMBER": "123",
"SEMIMAJOR_AXIS": "7147.915",
"PERIOD": "100.237",
"APOGEE": "847.311",
"PERIGEE": "692.250"
}
]
```
