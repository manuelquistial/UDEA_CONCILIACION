<?php

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;
use App\Usuario;

class UsuarioSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        $usuario = new Usuario();
        $usuario->nombre_apellido = "Manuel Alejandro Quistial Jurado";
        $usuario->email = "manuel.quistial@udea.edu.co";
        $usuario->telefono = "3117483498";
        $usuario->cedula = "1113533874";
        $usuario->usuario = "1113533874";
        $usuario->password = Hash::make("1113533874", [
            'rounds' => 12,
        ]);
        $usuario->estado_id = 4;
        $usuario->save();
        $usuario
                ->role()
                ->attach(1);
        
    }
}