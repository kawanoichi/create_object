<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>3Dオブジェクト生成ツール</title>
  <link rel="stylesheet" href="css/home_style.css">
  
  <!-- 自動更新 -->
  <!-- <meta http-equiv="refresh" content="5; URL="> -->

</head>
<body>
  <!-- Header -->
  <header class="header">
    <h1>3Dオブジェクト生成ツール</h1>
  </header>
  
  <!-- Main -->
  <div class="main">
    <div class="tool_header">
      <h1 class="tool_header_title">画像選択</h1>
      <h2 class="tool_header_subtitle">画像から3Dオブジェクトを生成</h2>
    </div>
    <div class="upload_bar">
      <!-- <form id="imageForm" enctype="multipart/form-data">
        <input type="file" name="image" accept="image/*">
        <button type="button" onclick="uploadImage()">画像をアップロード</button>
      </form> -->
      <form method="POST" action="/upload" enctype="multipart/form-data">
      @csrf
      <input type="file" name="image">
      <button>アップロード</button>

      <!-- 様々なPython実行方法 -->
      <br>
      <br>
      <a href="http://localhost:8000/home/execute">a tag Python Execute</a>
      <br>
      <br>
      <!-- <button onclick="loction.href='localhost:8000/home/execute'">button tag Python Execute</button> -->
      <form action="{{ url('/home/execute') }}" method="GET">
        <button type="submit">コントローラーを実行</button>
      </form>



</form>
    </div>
  </div>
  
  <!-- Footer -->
  <footer class="footer">
    <h1>FOOTER</h1>
  </footer>

</body>
</html>