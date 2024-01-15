<!-- storage/app/public/data/default.png" -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JavaScript Example</title>
    <!-- jQueryのCDNを読み込む -->
    <script src="https://code.jquery.com/jquery-3.6.4.min.js"></script>
</head>
<body>
    <!-- フォームで選択した画像 -->
    <img id="img" accept="image/*" src="default.png">

    <div class="buttons">
        <!-- フォーム -->
        <input type="file" name="logo" id="form" accept=".jpg, .jpeg, .png, .gif">

        <!-- 画像削除ボタン -->
        <button type="button" id="delete">削除</button>
    </div>

    <script>
        // 画像切り替え時にプレビュー表示
        $('#form').on('change', function (e) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $("#img").attr('src', e.target.result);
            }
            reader.readAsDataURL(e.target.files[0]);
        });
    </script>
</body>
</html>
