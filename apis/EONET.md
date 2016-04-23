# EONET, GIBSなどについて

- APIについて
  - http://eonet.sci.gsfc.nasa.gov/docs/v2.1
    - categoryを指定してeventをとってくることができる
    - 直近X件など指定できる. 直近Y日と日付指定も. statusがopenかclosedか(eventが終了したかどうか)でもfilterできる.
    - pointの場合はcoordinatesはlongitude, latitudeで返ってくる.
    - http://eonet.sci.gsfc.nasa.gov/api/v2.1/categories/10
      とすると"Severe Storms"が返ってきて衛星と同じように動きに時間変化があるからおもしろいかも?

  - 地球の画像について
    - http://map1.vis.earthdata.nasa.gov/wmts-geo/MODIS_Terra_CorrectedReflectance_TrueColor/default/2012-07-09/EPSG4326_250m/6/1/1.jpg
     などを叩く 
    - '2012-07-09'の部分を実際の日付にする http://hogehoge...{ZoomLevel}/{TileRow}/{TileCol}.pngという形式になっている 
    - row, columnは以下のページのようになっている
      - https://knowledge.safe.com/articles/180/which-web-map-tiling-scheme-should-i-use.html
    
