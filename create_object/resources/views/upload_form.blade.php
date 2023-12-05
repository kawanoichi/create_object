<!-- resources/views/image/upload_form.blade.php -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Upload</title>
</head>
<body>
    <h1>Image Upload</h1>

    <form action="/upload" method="post" enctype="multipart/form-data">
        @csrf
        <input type="file" name="image" accept="image/*" required>
        <button type="submit">Upload Image</button>
    </form>
</body>
</html>
