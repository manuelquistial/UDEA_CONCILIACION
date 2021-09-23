<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Usuario;
use App\Roles;
use Auth;

class ListUsersController extends Controller
{
    /**
     * Create a new controller instance.
     *
     * @return void
     */
    public function __construct(){
        $this->middleware('auth');
    }

    public function index(){

        $role = new Roles();
        $users = $role->usuarioByRole(1)
                    ->select('tr_usuarios.nombre_apellido','tr_usuarios.email')
                    ->get();

        return view('list_users', compact('users'));
    }
}
