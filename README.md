# English
## Simulation of the utilities of each policy for COVID-19
This repository was created to get experimental result for the advent calendar.

I thought it would be an interesting material to consider to what policy is would be beneficial that  simulating some policies(lockdown, distribute PCR test kit) and evaluate these result.

The initial version is limited in time(Because of I come up with idea two days before the deadline).

So, there are likely to be problems with readability of the code, messed structured, and so on.

**If you are interested, please contribute to this project. Send me pull request**

The license is MIT, So you can fork it and use it yourself.

I speak English as a second language. if you do not make sense my writings, you can ask me on issue board.
### Environment
- Docker version 19.03.13

### setting
```
docker-compose up -d
```

### execute simulate code
```
docker exec -it covid19-simulation-python bash
python main.py
```

# 日本語
## COVID-19に対する政策の効用シミュレーション
本リポジトリはアドベントカレンダー用の実験結果生成のために作ったリポジトリです。
昨今各国が行っているロックダウン政策や、PCRの検査キットの配布についてシミュレーションを行い。どういった政策が有益なのかを考察するための
材料になると面白いと思い、作りました。
初期版は時間に制約があり、コードの可読性・正確性・シミュレーションの現実に対する再現性について問題がある可能性が高いため、ぜひ興味を持ったら
プルリクエストを送ってもらえると嬉しいです。
ライセンスはMITであるため、自身でフォークしていただいて利用して頂いてもかまいません。

### 環境
- Docker version 19.03.13

### 環境構築
```
docker-compose up -d
```

### 実験スクリプト実行
```
docker exec -it covid19-simulation-python bash
python main.py
```
