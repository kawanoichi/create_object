<!-- resources/views/image/upload_form.blade.php -->
<!-- css path: /var/www/html/public/css -->
<!-- json path: /var/www/html/public/category.json -->
<!-- json path: /var/www/html/create_object_py/src/category.json -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <!-- 異なるデバイスの画面サイズに適応 -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- 外部CSSの読み込み -->
    <link rel="stylesheet" href="css/upload_form.css" type="text/css"> 
    <title>Image Upload</title>

    <!-- <script src="https://code.jquery.com/jquery-3.6.4.min.js"></script>
    <script>
        $(document).ready(function(){
            // JSONファイルを読み込む
            $.getJSON("category.json", function(data){
                // キーと値を表示する
                var list = $("<ul></ul>");
                $.each(data, function(key, value){
                    var listItem = $("<li>" + key + ": " + value + "</li>");
                    list.append(listItem);
                });

                // HTML内の特定の要素に結果を追加
                $("#jsonValues").append(list);
            });
        });
    </script> -->
</head>


<body>
    <!-- Header -->
    <div calss="header">
        <h1>Header</h1>
    </div>
    
    <!-- Main -->
    <div calss="main">
        <h1>
            Main
        </h1>
        
        <!-- jsonファイルのデータを出力 -->
        <!-- <div id="jsonValues"></div> -->
    
        <div class = "upload">
            <h2>Image Upload</h2>
            <form method="post" action="/upload" enctype="multipart/form-data">
                @csrf
                <!-- 画像のアップロードボタン -->
                <input type="file" name="image" accept="image/*">
                <br>
                
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
    </div>
</body>
</html>
