<?php

use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "web" middleware group. Make something great!
|
*/
use App\Http\Controllers\PythonController;
use App\Http\Controllers\ImageController;

Route::get('/', function () {
    return view('welcome');
});

// http://localhost:8000/home
// Route::get('/home', function () {
//     return view('home');
// });

Route::get('/upload-form', [ImageController::class, 'showForm']);
Route::post('/upload', [ImageController::class, 'upload']);
Route::get('/download/{imageName}', [ImageController::class, 'download'])->name('download');
