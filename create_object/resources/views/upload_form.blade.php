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
    <meta http-equiv="refresh" content="5"> 
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
    <div calss="main">
        <div class = "upload">
            <h1>画像アップロード</h1>
            <form method="post" action="/upload" enctype="multipart/form-data">
                @csrf
                <!-- 画像のアップロードボタン -->
                <label for="inputImage" class="custom-image-input">
                    画像ファイルを選択
                </label>
                <input type="file" id="inputImage" name="image" accept="image/*">
                <br>
                
                <h2>オブジェクトのカテゴリを選択してください</h2>
                <!-- ラジオボタン -->
                <input type="radio" name="selectCategory" value="0"> Airplane
                <br>
                <input type="radio" name="selectCategory" value="1"> Table
                <br>
                <input type="radio" name="selectCategory" value="2"> Chair
                <br>
                <button type="submit">アップロード</button>
            </form>
        </div>
    </div>

    <!-- Footer -->
    <div calss="footer">
        <h1>Footer</h1>
        <p>aaa</p>
    </div>
</body>
</html>

