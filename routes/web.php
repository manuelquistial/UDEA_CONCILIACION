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

Route::get('/', 'UploadFileController@index')->name('home');
Route::post('/file-upload', 'UploadFileController@fileUploadPost');
Route::get('/conciliacion', 'UploadFileController@downloadConciliacion');
Route::get('/reservas', 'UploadFileController@downloadReservas');
Route::get('/download', 'UploadFileController@download');
Route::get('/users', 'ListUsersController@index')->name('list_users');
Route::get('/porcentajes', 'PorcentajeController@index')->name('list_porcentajes');
Route::post('/porcentajes/update', 'PorcentajeController@update')->name('update_porcentajes');
