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
    <script src="https://code.jquery.com/jquery-3.6.4.min.js"></script>
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
                    <img id="img" accept="image/*" src="storage/app/public/data/default.png">
                    <p id="image_selection_text">画像を選択</p>
                </label>
                <input id="image_button" type="file" name="image" accept=".png, .jpeg, .jpg">
            <!-- <p>選択されていません</p> -->
            
            <br>
            <p>オブジェクトのカテゴリを選択</p>
            <!-- ラジオボタン -->
            <div class="select_category">
                <ul>
                <li>
                    <input class="radio" id="radio1" type="radio" name="selectCategory" value="0" checked>
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
            <label for="start_button" class="start-button">
                <p>変換開始</p>
            </label>
            <button id="start_button" type="submit" onclick="checkImage()">実行</button>
        </form>
    </div>

    <script>
        // 画像切り替え時にプレビュー表示
        $('#image_button').on('change', function (e) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $("#img").attr('src', e.target.result);
                // 画像が選択されたら<img>を表示し、<p>を非表示にする
                $("#img").show();
                // 画像が選択されたら<p>を非表示にする
                $("#image_selection_text").hide();
            }
            reader.readAsDataURL(e.target.files[0]);
        });
    
    
        function checkImage() {
            // alert('aa');
            // フォームの画像要素を取得
            var imageInput = document.getElementById('image_button');
            // 選択されたファイルがあるかどうかを確認
            if (imageInput.files.length === 0) {
                // ファイルが選択されていない場合はアラートを表示
                alert('画像を選択してください。');
            } else {
                // フォームを送信
                document.getElementById('imageForm').submit();
            }
        }
    </script>
    
    <!-- Footer -->
    <!-- <div class="footer">
        <h1>Footer</h1>
    </div> -->
    
</body>
</html>

