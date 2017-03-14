# igapico

## データベースの役割(要相談)
models.pyに書き込んでいるモデルの説明
- User
  - username
    - 登録されたユーザの名前
  - starttime
    - その人がゲーム開始した時間、今は名前を登録した時間
  - finishtime
    - ゲームを終えた時間
  - hint1_1
    - treasure1に対するhint1を見た時間
  - treasure1
    - 宝1を取ったか取ってないか or 取った時間

- Treasure_Beacon
  - treasure
    - 何番の宝か
  - beacon
    - その宝のビーコン番号

- Shop_Beacon
  - shopname
    - もし店名で選ばせるならここに店名
  - shop_id
    - 店名→番号に変換してから送るならここに店ID
  - beacon
    - その店が選ばれたときに返すビーコン番号

- Beacon
  - beacon
    - ビーコン番号
  - major
    - そのビーコンのmajor値
  - minor
    - そのビーコンのminor値

- Hint
  - hint_num
    - ヒント番号1-1とかになるのかな？
  - hint_sent
    - ヒントの文章

- Data
  - テストで作ったやつ


## テストで作った関数(要検証)
views.pyにいくつかの関数を追加しました。
- post_test
  - テスト用のやつですね

- pico_login
  - ユーザ登録機能(registerとかのほうがよかったかな)
    - ポストされた名前に対してデータベースにあるか探して、あったらすでにあるよって返して、なかったら新しくUserモデルのデータベースを作る、この時の時間をUser.objects.starttimeに格納

- shop_connect
  - 選んだ店と対応するビーコンを返すやつ(返す機能まだ)
    - ポストされた店名(店ID)が入った配列を見て、ビーコン番号が入った配列を作る。コメントアウトの位置を変えれば店名でポストされた配列に対応できるはず。

- treasure_check
  - どの宝を取ったかをUserオブジェクトに格納(これ一番怪しい)
    - ポストされた名前と宝番号に合わせて、Userオブジェクトのアップデートを行う
