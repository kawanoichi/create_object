<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
// use Illuminate\Support\Facades\Artisan;

class PythonController extends Controller
{
    public function runPythonScript()
    {
        // Pythonスクリプトを実行するコマンド
        $output = [];
        $returnCode = 0;
        exec('python3 /var/www/html/src/test.py',
            $output, $returnCode);

        $pythonResult = implode("<br>", $output);
        return $pythonResult;
    }
}
