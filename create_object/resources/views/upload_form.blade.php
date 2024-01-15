<!-- resources/views/image/upload_form.blade.php -->
<!-- css path: /var/www/html/public/css -->
<!-- json path: /var/www/html/public/category.json -->
<!-- json path: /var/www/html/create_object_py/src/category.json -->
<!-- NOTE: CSSが反映されない場合,キャッシュを強制的にクリアする >> (Shift + F5) -->
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- 文字コード -->
    <meta charset="UTF-8">
    <!-- 自動更新 -->
    <!-- <meta http-equiv="refresh" content="3">  -->
    <!-- 異なるデバイスの画面サイズに適応 -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- 外部CSSの読み込み -->
    <link rel="stylesheet" href="css/upload_form.css" type="text/css"> 
    <title>Image Upload</title>
</head>

<body>
    <!-- Header -->
    <div class="header">
        <h1>３Ⅾオブジェクト生成ツール</h1>
    </div>

    <!-- Main -->
    <div class="main">
        <h1>画像から3Dオブジェクト(PLYファイル)に変換</h1>

        <form class = "upload" method="post" action="/upload" enctype="multipart/form-data">
            <!-- 画像のアップロードボタン -->
            <p>画像のアップロード</p>
            @csrf
            <label for="image_button" class="custom-image-input">
                <p>画像を選択</p>
            </label>
            <input id="image_button" type="file" name="image" accept="image/*">
            <!-- <p>選択されていません</p> -->
            
            <br>
            <p>オブジェクトのカテゴリを選択</p>
            <!-- ラジオボタン -->
            <div class="select_category">
                <ul>
                <li>
                    <input class="radio" id="radio1" type="radio" name="selectCategory" value="0">
                    <label for="radio1">Airplane</label>
                    <div class="check"></div>
                </li>
                
                <li>
                    <input class="radio" id="radio2" type="radio" name="selectCategory" value="1">
                    <label for="radio2">Table</label>
                    <div class="check"></div>
                    <!-- <div class="check"><div class="inside"></div></div> -->
                    
                </li>
                
                <li>
                    <input class="radio" id="radio3" type="radio" name="selectCategory" value="2">
                    <label for="radio3">Chair</label>
                    <div class="check"></div>
                    <!-- <div class="check"><div class="inside"></div></div> -->
                </li>
                </ul>
            </div>
            <button type="submit">実行</button>
        </form>
<!--     
        <p>
        この下に JavaScript を使って文字列を出力します。
        </p>

        <script src="css/sample.js">
        </script> -->

</div>

    <!-- Footer -->
    <!-- <div class="footer">
        <h1>Footer</h1>
    </div> -->
    
</body>
</html>

