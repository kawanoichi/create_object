// 画像切り替え時にプレビュー表示
$('#form').on('change', function (e) {
    var reader = new FileReader();
    reader.onload = function (e) {
        $("#img").attr('src', e.target.result);
    }
    reader.readAsDataURL(e.target.files[0]);
});

// 削除ボタンクリック時にフォームとプレビューを初期化
// $('#delete').on('click', function (e) {
//   $("#img").attr('src', 'https://tool-engineer.work/wp-content/uploads/2022/06/default.png');
//   $("#form").val('');
// });