<!-- resources/views/image/upload_form.blade.php -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Upload</title>
</head>
<body>
    <div class = "upload">
        <h1>Image Upload</h1>
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
</body>
</html>
