<?php

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Auth::routes();

Route::get('activate/{token}', 'Auth\RegisterController@activate')
    ->name('activate');
Route::get('/home', 'HomeController@index')->name('home');
Route::get('/', 'UploadFileController@index');
Route::post('/file-upload', 'UploadFileController@fileUploadPost');
Route::get('/conciliacion', 'UploadFileController@downloadConciliacion');
Route::get('/reservas', 'UploadFileController@downloadReservas');
Route::get('/download', 'UploadFileController@download');

Auth::routes();

Route::get('/home', 'HomeController@index')->name('home');
