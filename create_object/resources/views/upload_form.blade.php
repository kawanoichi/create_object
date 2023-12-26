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
    <meta http-equiv="refresh" content="3"> 
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
        <!-- 以下 -->
        <div id="clock"></div>

        <script>
        function updateClock() {
            var now = new Date();
            var hours = now.getHours();
            var minutes = now.getMinutes();
            var seconds = now.getSeconds();

            // ゼロパディングを追加
            hours = hours < 10 ? '0' + hours : hours;
            minutes = minutes < 10 ? '0' + minutes : minutes;
            seconds = seconds < 10 ? '0' + seconds : seconds;

            var timeString = hours + ':' + minutes + ':' + seconds;
            
            // HTML要素に挿入
            document.getElementById('clock').innerText = timeString;
        }
        // 初回表示
        updateClock();
        </script>
        <!-- 以上 -->

        <form class = "upload" method="post" action="/upload" enctype="multipart/form-data">
            <!-- 画像のアップロードボタン -->
            <p>画像のアップロード</p>
            @csrf
            <label for="inputImage" class="custom-image-input">
                画像ファイルを選択
            </label>
            <input id="image_button" type="file" id="inputImage" name="image" accept="image/*">
            <br>
            
            <p>オブジェクトのカテゴリを選択してください</p>
            <!-- ラジオボタン -->
            <input id="radio" type="radio" name="selectCategory" value="0"> Airplane
            <br>
            <input id="radio" type="radio" name="selectCategory" value="1"> Table
            <br>
            <input id="radio" type="radio" name="selectCategory" value="2"> Chair
            <br>
            <button type="submit">アップロード</button>
        </form>
    
        </div>
    </div>

    <!-- Footer -->
    <div class="footer">
        <h1>Footer</h1>
    </div>
    
</body>
</html>

