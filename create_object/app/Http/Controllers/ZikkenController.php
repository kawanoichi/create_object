<?php
namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;


class ZikkenController extends Controller
{
    public function showForm()
    {
        return view('zikken');
    }
}