# NLP.md

botの発言に関する調査をまとめる。

## IBM Bluemix

### 所感

あんまり目欲しいツールやAPIはない。
日本語対応していないものが多い。

### WatsonAPI

https://console.au-syd.bluemix.net/docs/services/watson.html

- AlchemyAPI: 機械学習ツール群(テキスト解析・画像解析) http://www.alchemyapi.com/products/demo/alchemylanguage
- Concept Expansion
- Dialog: ルールベース対話処理
- Document Conversion: HTML, PDF, Wordなど相互変換する
- Language Translation: 機械翻訳
- Natural Language Classifier: 文書分類
- Personality Insight: 文体だったり文を書いた人の特性を当てる
- Relationship Extraction
- Retrival and Rank: 文書検索
- Speech to Text: 音声認識
- Text to Speech: 音声合成 
- Tone Analyzer: 感情・文体などなどを当てる
- Tradeoff Analystics: トレードオフの可視化
- Visual Recognition: 一般物体認識

### 参考リンク

- [Bluemix コンソール](https://console.ng.bluemix.net/?direct=classic)
- [IBM Bluemixご紹介](http://www.slideshare.net/YusukeMorizumi1/nasa-space-apps-challenge-input-day-bluemi)
- [より詳細なページ](http://joohoun.jimdo.com/2016/04/06/space-apps-challenge-tokyo-2016%E5%90%91%E3%81%91ibm-bluemix%E6%83%85%E5%A0%B1%E3%81%BE%E3%81%A8%E3%82%81/)
- [より詳細なページ](http://joohoun.jimdo.com/2016/04/06/space-apps-challenge-tokyo-2016%E5%90%91%E3%81%91ibm-bluemix%E6%83%85%E5%A0%B1%E3%81%BE%E3%81%A8%E3%82%81/)

## 発言方法について

### 場所をつぶやく

ツイートをとってきて(1)、
```
札幌に来たよー
```
場所の部分をテンプレート化してやる(2)と、
```
{{place}}に来たよー
```
placeの部分を入れ替えてやる(3)だけで、
```
$place="上海"
上海に来たよー
```
なんか喋ってる風になる。

1. TwitterAPIかBluemixのAPIを使う。
2. NamedEntityRecognition(NER)で場所の単語を抽出。NERにはKNBを使う。
3. 緯度経度情報から地名に変換した結果を埋め込む。

(1), (2)は、事前に準備しておいて、(3)は実行時。

