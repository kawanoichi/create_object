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

    public function upload2(Request $request)
    {
    if ($request->has('selectCategory')) {
        $selectedOption = $request->input('selectCategory');
        echo "ラジオボンタン選択肢:" . $selectedOption . "<br>";
    } else {
        echo "失敗";
    }
    return;
    }

    public function upload(Request $request)
    {
        $developFlag = True;
        $developFlag = False;
        $errorFlag = False;

        // カテゴリの受付
        if ($request->has('selectCategory')) {
            $selectedOption = $request->input('selectCategory');
            echo "ラジオボンタン選択肢:" . $selectedOption . "<br>";
        } else {
            return "カテゴリーを選択して下さい<br>";
        }
    
        // バリデーションするためのメソッド
        // 'required': 画像が必須であることを示します。
        // 'image': 画像であることを確認します。
        // 'mimes:jpeg,png,jpg,gif,svg': 画像の許可される拡張子を指定しています。
        // 'max:2048': アップロードされる画像の最大サイズを制限しています（2048キロバイトまで）。
        $request->validate([
            // 'image' => 'required|image|mimes:jpeg,png,jpg,gif,svg|max:2048',
            'image' => 'required|image|mimes:jpeg,png,jpg,gif',
        ]);
        
        $image_path = $request->file('image');
        // 画像名を自動的な名前に変更
        $imageName = time().'.'.$image_path->extension();
        
        // 画像を "storage/app/public/data" ディレクトリに保存
        $image_path->storeAs('public/data', $imageName);

        if ($developFlag) {
            echo " imageName: " . $imageName . "<br>";
            echo "image_path: " . $image_path . "<br>";
        }

        // 画像アップロード成功確認
        if (file_exists($image_path)) {
            if ($developFlag) {
                echo "upload: success<br>";
            }
        } else {
            $errorFlag = True;
            echo "upload: failed<br>";
        }

        // パスの作成
        $executePythonCommand = 'python3 /var/www/html/create_object_py/src';
        
        // Pythonスクリプトを実行
        $output = [];
        $returnCode = 0;
        exec("{$executePythonCommand} {$imageName} {$selectedOption}", $output, $exitCode);
        
        if ($developFlag) {
            echo "python ----------------------------------------------<br>";
            if ($exitCode !== 0) {
                // 実行に失敗
                $errorFlag = True;
                echo "Python execute: failed<br>";
                echo "Exit code: " . $exitCode . "<br>";
                $pythonResult = implode("<br>", $output);
                echo "Error output:<br>" . $pythonResult;
                echo $pythonResult;
            } else {
                // 成功
                $pythonResult = implode("<br>", $output);
                if ($developFlag) {
                    echo "Python execute: success<br>";
                    echo $pythonResult;
                }
            }
            echo "----------------------------------------------------<br>";
        }
            

        // 変換後の画像ファイル名
        $outputFileName = $imageName[-1];
        if ($errorFlag){
            return "<br>失敗";
        }else{
            return redirect()->route('download', $imageName);
        }
    }
    
    public function download($imageName)
    {
        // ※この関数で文字列をechoするとダウンロードできなくなる
        $extension = pathinfo($imageName, PATHINFO_EXTENSION);
        $plyFileName = str_replace($extension, 'ply', $imageName);
        $path = storage_path("app/public/data/{$plyFileName}");
        if (file_exists($path)) {
            return response()->download($path, $plyFileName);
        } else {
            echo "File not found". $path . "<br>";
            return "download: failed<br>";
        }
    }

    public function testExecutePython()
    {
        // Pythonスクリプトを実行するコマンド
        // $output = [];
        // $returnCode = 0;
        // exec('python3 /var/www/html/src/test.py', $output, $returnCode);

        // $pythonResult = implode("<br>", $output);
        // return $pythonResult;
        return "実験";
    }


}
