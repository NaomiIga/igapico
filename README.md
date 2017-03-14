# igapico

## データベースの役割(要相談)
models.pyに書き込んでいるモデルの説明
- User
  - username
    -登録されたユーザの名前
  - starttime
    - その人がゲーム開始した時間、今は名前を登録した時間
  - finishtime
    - ゲームを終えた時間
  - hint1_1
    - treasure1に対するhint1を見た時間
  - treasure1
    - 宝1を取ったか取ってないか or 取った時間
