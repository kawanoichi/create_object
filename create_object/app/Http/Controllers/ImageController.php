<?php

// namespace App\Http\Controllers;

// use Illuminate\Http\Request;

// class ImageController extends Controller
// {
//     // 画像を保存するメソッド
//     public function upload(Request $request)
//     {
//         // ディレクトリ名
//         $dir = 'image_data';

//         // sampleディレクトリに画像を保存
//         $request->file('image')->store('public/' . $dir);

//         return redirect('/');
//     }
// }

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
        $request->validate([
            'image' => 'required|image|mimes:jpeg,png,jpg,gif,svg|max:2048',
        ]);

        $image = $request->file('image');
        $imageName = time().'.'.$image->extension();

        // 画像をstorage/app/publicディレクトリに保存
        $image->storeAs('public', $imageName);

        // Pythonスクリプトを呼び出し
        $output = [];
        $returnCode = 0;
        $pythonScriptPath = 'python3 /var/www/html/src/read_image.py';
        exec($pythonScriptPath, $output, $returnCode);

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
}
