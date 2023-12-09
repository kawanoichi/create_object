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
        // $executePythonCommand = 'python3 /var/www/html/src/read_image.py';
        // $executePythonCommand = 'cd /var/www/html/create_object_py && make run';
        // $executePythonCommand = 'cd /var/www/html/create_object_py && python3 -V';
        // $executePythonCommand = 'cd /var/www/html/create_object_py && poetry -V';
        // $executePythonCommand = 'cd /var/www/html/create_object_py && poetry -V';
        // $executePythonCommand = 'ls /root/.local/bin/poetry';
        // $executePythonCommand = 'ls /root/.pyenv/shims/python3';
        $executePythonCommand = 'which poetry';
        // $executePythonCommand = 'pwd';
        // $executePythonCommand = 'ls /usr/bin';
        // $executePythonCommand = 'cd /var/www/html/create_object_py && poetry run python3 -m src airplane.png';
        
        // // Pythonスクリプトを呼び出し
        $output = [];
        $returnCode = 0;
        exec("$executePythonCommand", $output, $returnCode);
        // exec("{$executePythonCommand} {$this->imageDirPath}/{$imageName}", $output, $returnCode);

        if ($returnCode !== 0) {
            // エラーが発生した場合
            $errorMessage = implode("\n", $output);
            \Log::error('Python Script Output: ' . implode("\n", $output));
            return response()->json(['error' => $errorMessage], 500);
        }

        // $outputに"FileCheck-14"が含まれているかチェック
        // if (strpos(implode("\n", $output), 'poetry') !== false) {
        //     // "FileCheck-14"が含まれている場合の処理
        //     \Log::info('FileCheck-14 found in output');
        //     return "True";
        // } else {
        //     // "FileCheck-14"が含まれていない場合の処理
        //     \Log::info('FileCheck-14 not found in output');
        //     return "False";
        // }
        
        return $output;

        // // Pythonスクリプトのパス
        // $pythonScriptPath = base_path('/var/www/html/create_object_py/src/read_image.py');

        // // Poetryでスクリプトを実行するコマンド
        // $command = "poetry run python $pythonScriptPath";

        // // 実行
        // $output = shell_exec($command);

        // // 結果の出力
        // dd($output);


        // $pythonResult = implode("<br>", $output);
        // return $pythonResult;

        // 変換後の画像ファイル名
        $imageName = time().'.'.$image->extension();
        $outputFileName = $imageName[-1];

        // return redirect()->route('download', $imageName);
    }
    
    public function download($filename)
    {
        $path = storage_path("app/public/data/{$filename}");

        if (file_exists($path)) {
            return response()->download($path, $filename);
        } else {
            return response()->json(['error' => 'File not found.'], 404);
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
