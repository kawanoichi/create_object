<?php
namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;

class ImageController extends Controller
{
    public function showForm()
    {
        return view('upload_form');
    }
    
    public function upload(Request $request)
    {
        // バリデーションするためのメソッド
        // 'required': 画像が必須であることを示します。
        // 'image': 画像であることを確認します。
        // 'mimes:jpeg,png,jpg,gif,svg': 画像の許可される拡張子を指定しています。
        // 'max:2048': アップロードされる画像の最大サイズを制限しています（2048キロバイトまで）。
        $request->validate([
            // 'image' => 'required|image|mimes:jpeg,png,jpg,gif,svg|max:2048',
            'image' => 'required|image|mimes:jpeg,png,jpg,gif',
        ]);


        $image = $request->file('image');
        // 画像名を自動的
        // $image->extension() : 拡張子を返す
        $imageName = time().'.'.$image->extension();
        
        // 画像をstorage/app/public/image_dataディレクトリに保存
        $image->storeAs('public/image_data', $imageName);

        // パスの作成
        $imageDirPath = '/var/www/html/storage/app/public/image_data';
        $executePythonCommand = 'python3 /var/www/html/src/read_image.py';
        
        // Pythonスクリプトを呼び出し
        $output = [];
        $returnCode = 0;
        exec("{$executePythonCommand} {$imageDirPath}/{$imageName}", $output, $returnCode);
        if ($returnCode !== 0) {
            // エラーが発生した場合
            $errorMessage = implode("\n", $output);
            return response()->json(['error' => $errorMessage], 500);
        }

        $pythonResult = implode("<br>", $output);
        return $pythonResult;

        // 変換後の画像ファイル名
        // $convertedImageName = $output[0];

        // return redirect()->route('download', $convertedImageName);
    }
    
    public function download($imageName)
    {
        $imagePath = storage_path("app/public/{$imageName}");

        if (file_exists($imagePath)) {
            return response()->download($imagePath);
        } else {
            abort(404);
        }
    }

    public function testExecutePython()
    {
        // Pythonスクリプトを実行するコマンド
        $output = [];
        $returnCode = 0;
        exec('python3 /var/www/html/src/test.py', $output, $returnCode);

        $pythonResult = implode("<br>", $output);
        return $pythonResult;
    }


}
