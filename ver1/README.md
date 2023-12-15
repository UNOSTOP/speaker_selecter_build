# speaker_selecter ver4

" speaker_selecter ver3 "を参考に、Raspberry Pi OSのインストールからサーバー構築までの詳細をまとめたものです。また、GPIOの役割のみ持つピンだけを使用するように" setting.toml "を大幅に変更しました。

# 環境構築工程

1. **OSのインストール**
2. **Wi-Fi, proxyの設定**
3. **speaker_selecterを使う**
4. **speaker_selecterの自動起動**
5. **7インチタッチディスプレイの設定（おまけ）**

# 1. OSのインストール

[**公式**](https://www.raspberrypi.com/software/)からRaspberry Pi Imagerをインストールしてください。その後、Imagerを開きOSをSDカードにインストールしてください。以下は、現在のOSのバージョンです。（　[**過去バージョンのOSはこちら**](https://raspida.com/old-raspbian-download#index_id0)　）

* **Raspberry Pi OS (Legacy) Lite**
* **Release date**: December 5th 2023
* **System**: 32-bit
* **Kernel version**: 6.1
* **Debian version**: 11 (bullseye)
* **Size**: 363MB

# 2. Wi-Fi, proxyの設定

## 2.1 Wi-Fi

" conf_files " 内の " wpa_supplicant.conf "と" dhcpcd.conf "を参考にし、以下に示すパスに置かれている同名ファイルに変更を加えてください。

* wpa_supplicant.conf >>> /home/pi/etc/wpa_supplicant/wpa_supplicant.conf
* dhcpcd.conf >>> /home/pi/etc/dhcpcd.conf

```shell
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

## 2.2 proxy

" conf_files " 内の " apt.conf "と" .bashrc "を参考にし、以下に示すパスに置かれている同名ファイルに変更を加えてください（" apt.conf "は新規作成）。

* apt.conf >>> /home/pi/apt/apt.conf
* dhcpcd.conf >>> /home/pi/.bashrc

上記の変更を終えたら、一度再起動を行いWi-Fiの接続確認を行ってください。

# 3. speaker_selecterを使う

以下のコマンドで、Githubから " speaker_selecter " フォルダをコピーしてください。

```shell
cd ~
sudo git clone https://github.com/kudolab/speaker_selecter.git
```

※ " git " コマンドがないと怒られた場合、以下のコマンドでインストールしてから、やり直してください。

```shell
sudo apt-get update
sudo apt-get install git
```

次に、以下のコマンドで、pythonの仮想環境を構築します。

```shell
sudo apt-get install python3-venv
cd speaker-selecter/ver4
sudo python3 -m venv venv
. ./venv/bin/activate
# from here, (venv) is activate.
(venv):sudo venv/bin/pip3 install -r requirements.txt
# check if it's installed.
(venv):pip3 list
(venv):deactivate
```

最後に、 " app.py " を実行し、動作を確認します。

```shell
cd speaker-selecter/ver4
sudo venv/bin/python3 app.py
```

実行後、同じWi-Fiに接続されたデバイスを使いサーバーと交信ができるかを確認する。

```shell
curl http://172.24.184.114/health
# return "ok(^^)b"
curl -X PUT -H "Content-Type: application/json" -d '{"speaker_num":5}' 172.24.184.114/speaker
# return "speaker_num changed to {5}"
curl http://172.24.184.114/speaker
# return "{"speaker_num": 5}"
```

# 4. speaker_selecterの自動起動

以下のコマンドで、" conf_files " 内の " speaker-selecter.service " を " /etc/systemd/system " に移動してください。

```shell
cd ~
sudo cp -r /speaker_selecter/ver4/conf_files/speaker-selecter.service /etc/systemd/system/speaker-selecter.service 
```

次に、サービスの再読み込み、有効化、開始を行い起動状態が " active " になっていることを確認してください。

```shell
# 再読み込み
sudo systemctl daemon-reload
# 有効化
sudo systemctl enable speaker-selecter
# 開始
sudo systemctl start speaker-selecter
# 起動状態の確認
sudo systemctl status speaker-selecter 
```

# 5. 7インチタッチディスプレイの設定（おまけ）

7インチタッチディスプレイの画面の回転、DSIとHDMIの出力設定を " /boot/config.txt "に以下のコードを追加してください。

```shell
sudo nano /boot/config.txt
```
```
# 回転
lcd_rotate=2
# hdmiの出力
hdmi_group:0=2
hdmi_mode:0=28
```
