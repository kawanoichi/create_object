<!-- resources/views/image/upload_form.blade.php -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Upload</title>
</head>
<body>

    <div class="upload">
        <!-- アップロード -->
        <h1>Image Upload</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
            @csrf
            <input type="file" name="image" accept="image/*" required>
            <button type="submit">Upload Image</button>
        
        </div>
        
        <br>
        
        <!-- カテゴリ選択 -->
        <fieldset>
        <legend>Select a class of object:</legend>
        <div>
            <input type="radio" id="huey" name="drone" value="airplane" checked />
            <label for="huey">Airplane</label>
        </div>

        <div>
            <input type="radio" id="dewey" name="drone" value="chair" />
            <label for="dewey">Chair</label>
        </div>

        <div>
            <input type="radio" id="louie" name="drone" value="table" />
            <label for="louie">Table</label>
        </div>
        </fieldset>
    
    </form>

</body>
</html>
