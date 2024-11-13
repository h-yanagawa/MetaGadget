# MetaGadget Getting Started

# device を用意する

MetaGadget を使って、cluster から接続する物理的なデバイスを用意しましょう。

今回は、マイクロコンピュータとして Rapberry Pi Zero 2 W を用意し、GPIO を使って LED を点灯させます。出来上がりのイメージとしては、cluster の中で、電球にインタラクトする(画面中でタップする)と、現実の LED が点灯するというガジェットを作ります。

# Raspberry Pi Zero 2 W と LED の接続

図のような回路を構成しておきます。

![circuit](https://github.com/user-attachments/assets/cdf78993-5c05-4ee5-b4da-3e92afdb4d1b)

# Raspberry Pi Zero 2 W のセットアップ

この先は、Raspberry Pi OS Lite をインストールしてある前提で話を進めます。

Raspberry Pi OS Lite のインストール方法についてはこちらを御覧ください。

必要パッケージのインストール

```bash
sudo apt-get install vim python3-dev

python -m venv venv
. venv/bin/activate
pip install metagadget RPi.GPIO
```

# ngrok アカウントの取得

MetaGadget を動かすためには、ngrok のアカウントのが必要です。無料で取得可能なので、[こちら](https://ngrok.com/)からアカウントを作成してください。作成した後に管理画面から、Auth Token と自分のアカウントに紐づけられたドメインを取得してください。

# Cluster からの Call External を受け取る Python プログラムを用意する

セットアップが出来たので、MetaGadget ライブラリを使ったプログラムを用意します。

```python
import RPi.GPIO as GPIO
from metagadget import MetaGadget

# PIN Number
LED_PIN = 14

# GPIO Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

def main():
    app = MetaGadget()

    @app.receive
    def handle(data):
        if data == "on":
            GPIO.output(LED_PIN, 1)
        else:
            GPIO.output(LED_PIN, 0)

    app.run()
    GPIO.cleanup()

if __name__ == "__main__":
    main()
```

用意したプログラムを次のような環境変数をセットして起動します。これらの環境変数は ngrok のの設定のために必要なものです。ngrok アカウント作成時に取得した Auth Token とドメインをそれぞれ指定してください。

```bash
NGROK_AUTHTOKEN="YOUR_NGROK_KEY"  NGROK_DOMAIN="YOUR_NGROK_DOMAIN" python main.py

WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5001
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: XXX-XXX-XXX
```

上記のようにメッセージが表示されれば起動しています。

cluster を使って確認を行う前に、curl を使って動作を確認してみましょう。次のコマンドで LED が点灯します。

```bash
curl -X POST -H 'Content-Type: application/json' -d '{"request": "on"}' https://YOUR_NGROK_DOMAIN/
```

今度は LED を消灯します。

```bash
curl -X POST -H 'Content-Type: application/json' -d '{"request": "off"}' https://YOUR_NGROK_DOMAIN/
```

点灯しない場合は、LED の回路が正しく接続されているか確認しましょう。また、raspberry pi のシェルにエラーメッセージが表示されていないかも確認しましょう。

# Craft Item の作成

Cluster Creator Kit が Setup されている Unity で Craft Item を作ります

まずは、簡単な球を Item として登録します。

Empty Game Object を作成し、Light という名前をつけます。

その配下に Sphere を作成しておきます。Hierachy 画面は以下のようになるはずです。

![hierachy](https://github.com/user-attachments/assets/20ccbed9-fbf2-41e7-8994-a00355da2f0c)
Scene 画面では Sphere だけが見えます。

![scene](https://github.com/user-attachments/assets/7ee41a28-d077-4f09-8e88-4a40ca0a30e3)

Empty GameObject である Light オブジェクトの Inspector 画面から、”Item(Script)” と “Scriptable Item (Script)” コンポーネントを追加しておきます。”Item(Script)”コンポーネントの設定で、Item Name と Size を指定するのを忘れないようにしましょう。“Scriptable Item (Script)”ではこのオブジェクトに紐づける Cluster Script を設定できますが、後ほど設定するのでこの場では空のままで問題ありません。

![inspector](https://github.com/user-attachments/assets/1704dee1-fde7-408b-be31-aa7d1697f76b)

アイテムが出来たら、upload が必要です。menu の Cluster > UploadCraftItem を選ぶと設定画面が現れます。

![UploadCraftItem](https://github.com/user-attachments/assets/69ae8f5a-c5f0-4c18-b310-200298420ad6)

この画面に、Prefab にしたアイテムを Drag&Drop すると Item が登録できます。Valid Item と表示されていたら、Upload を押して作ったアイテムを登録しましょう。

その後、callExternal の接続先を Unity のメニューから登録します。menu の Cluster > ExternalCommunication を選ぶと設定画面が現れます。先に ngrok で取得した自分のドメインを指定して、”https://YOUR_NGROK_DOMAIN/” という形で、URL を登録してください。

![ExternalCommunication](https://github.com/user-attachments/assets/98134e7b-5ea7-4681-a6d5-be4c209e05c3)

# Craft Item の設置

作ったアイテムを自分のワールドクラフトにおいてみましょう。

![putItem](https://github.com/user-attachments/assets/e2d0985d-f0e9-4b8a-b26b-a66364274064)

このアイテムにはスクリプトが登録されていないので、クラフトモードでアイテムを選択した状態で F12 を押してスクリプトを編集します。

```bash
let ledOn = false;
$.onInteract(() => {
  $.log("interacted.");
  if (ledOn) {
    ledOn = false;
    $.callExternal("off", "led");
  } else {
    ledOn = true;
    $.callExternal("on", "led");
  }
});

$.onExternalCallEnd((res, meta, err) => {
  $.log("external call end.");
  $.log(res); // デバッグ用にレスポンスを表示します
  $.log(meta); // デバッグ用にリクエスト時に指定しているmeta情報を表示します。"led" と表示されます
  $.log(err); // エラーが起きている場合このコードによりエラーが表示されます。
});
```

このスクリプトをアイテムに登録すると、球体をクリックすることで、LED の点灯、消灯を行うことができます。

これで、MetaGadget を使って Craft Item から現実のデバイスの制御を行う一連の流れが実装できました。
