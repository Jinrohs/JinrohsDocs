# EONETについて

- APIについて
  - http://eonet.sci.gsfc.nasa.gov/docs/v2.1
    - categoryを指定してeventをとってくることができる
    - 直近X件など指定できる. 直近Y日と日付指定も. statusがopenかclosedか(eventが終了したかどうか)でもfilterできる.
    - pointの場合はcoordinatesはlongitude, latitudeで返ってくる.
    - http://eonet.sci.gsfc.nasa.gov/api/v2.1/categories/10
      とすると"Severe Storms"が返ってきて衛星と同じように動きに時間変化があるからおもしろいかも?
