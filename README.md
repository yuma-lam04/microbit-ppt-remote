# microbit-ppt-remote

micro:bit を PowerPoint のプレゼンターリモコンとして使うための小さなツールです。
micro:bit のボタン操作をシリアル経由で PC に送り、PC 側スクリプトがキーボード入力に変換して PowerPoint を操作します。

## 構成

```
[micro:bit] --(USB Serial)--> [PC: Python script] --(Keyboard emulation)--> [PowerPoint]
```

- **micro:bit 側**: ボタン/ロゴタッチを検知してコマンド文字列をシリアル送信
- **PC 側**: シリアルを監視し、受信したコマンドに応じて対応するキーを叩く

## 操作対応表

| micro:bit の操作 | 送信コマンド | PC 側の動作 | PowerPoint での挙動 |
| --- | --- | --- | --- |
| A ボタン | `NEXT` | → キー | 次のスライド |
| B ボタン | `PREV` | ← キー | 前のスライド |
| A + B 同時押し | `BLACK` | `B` キー | 黒画面トグル |
| ロゴタッチ | `WHITE` | `W` キー | 白画面トグル |

チャタリング防止のため、micro:bit 側で 350ms のクールタイムを設けています。

## 必要なもの

- micro:bit 本体(v2 推奨)
- USB ケーブル
- Python 3.x がインストールされた PC
- PowerPoint(スライドショー実行中の状態)

## セットアップ

### 1. micro:bit 側の書き込み

`microbit/main.py` を [MakeCode エディタ](https://makecode.microbit.org/) の Python モードに貼り付けて、micro:bit にダウンロードしてください。

### 2. PC 側の依存パッケージをインストール

```bash
pip install pyserial pynput
```

### 3. シリアルポートの確認

micro:bit を USB 接続した状態で、デバイスマネージャー等から割り当てられている COM ポート番号を確認してください。
`pc/microbit_ppt_remote.py` の冒頭にある `PORT` を実際のポート名に書き換えます。

```python
PORT = "COM4"  # ← ここを自分の環境に合わせて変更
```

macOS / Linux の場合は `/dev/tty.usbmodemXXXX` のような名前になります。

## 使い方

1. PowerPoint でスライドショーを開始する
2. PC 側スクリプトを起動する

   ```bash
   python pc/microbit_ppt_remote.py
   ```

3. `Listening: COM4` と表示されたら準備完了
4. micro:bit のボタンを押してスライドを操作する

終了するときは PC 側のターミナルで `Ctrl + C` を押してください。

## ファイル構成

```
microbit-ppt-remote/
├── pc/
│   └── microbit_ppt_remote.py   # PC 側の受信スクリプト
├── microbit/
│   └── main.py                  # micro:bit 側のコード
└── README.md
```

## トラブルシューティング

- **`Listening:` の後に何も表示されない**: micro:bit のボタンを押しても反応がない場合、`PORT` の指定が正しいか、他のシリアル通信ソフト(MakeCode の Show Console など)がポートを掴んでいないかを確認してください。
- **キー入力が PowerPoint に届かない**: PowerPoint がアクティブウィンドウになっているか確認してください。バックグラウンドのままでは送信先になりません。
- **連打で誤作動する**: micro:bit 側の `cool` の値を大きくすると、より厳しく連打を弾けます。

## 今後の拡張アイデア

- 加速度センサーを使ったジェスチャー操作
- micro:bit の Radio 機能による無線化(送信機 + 受信機の 2 台構成)
- LED マトリクスへの経過時間表示
- 音量・メディアキー操作の追加

## ライセンス

MIT
