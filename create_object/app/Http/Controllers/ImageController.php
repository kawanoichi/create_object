<?php
namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;

class ImageController extends Controller
{
    protected $imageDirPath;

    public function __construct()
    {
        // コンストラクタで初期化
        $this->imageDirPath = '/var/www/html/storage/app/public/image_data';
    }

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
        
        // 画像をstorage/app/public/dataディレクトリに保存
        $image->storeAs('public/data', $imageName);

        // パスの作成
        // $executePythonCommand = 'python3 /var/www/html/public/check_library.py';
        $executePythonCommand = 'python3 /var/www/html/create_object_py/src';
        
        // Pythonスクリプトを呼び出し
        $output = [];
        $returnCode = 0;
        // exec("$executePythonCommand", $output, $returnCode);
        // exec("{$executePythonCommand} {$this->imageDirPath}/{$imageName}", $output, $returnCode);
        
        exec("{$executePythonCommand} {$imageName}", $output, $exitCode);
        if ($exitCode !== 0) {
            // 実行に失敗
            echo "Python script execution failed. Exit code: $exitCode\n";
            echo "Error output:\n" . implode("\n", $output);
        } else {
            // 成功
            echo "execute python is success";
            $pythonResult = implode("<br>", $output);
            // return $pythonResult;
        }


        // 変換後の画像ファイル名
        $imageName = time().'.'.$image->extension();
        $outputFileName = $imageName[-1];

        return redirect()->route('download', $imageName);
        // return "OK";
    }
    
    public function download($imageName)
    {
        $extension = pathinfo($imageName, PATHINFO_EXTENSION);
        // return $extension;
        $plyFileName = str_replace($extension, 'ply', $imageName);
        $path = storage_path("app/public/data/{$plyFileName}");
        if (file_exists($path)) {
            return response()->download($path, $plyFileName);
        } else {
            echo "File not found\n";
            return $plyFileName;
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
