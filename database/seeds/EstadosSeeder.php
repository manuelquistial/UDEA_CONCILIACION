<?php

use Illuminate\Database\Seeder;
use App\Estados;

class EstadosSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        $estado = new Estados();
        $estado->estado = "En proceso";
        $estado->estado_id = "1";
        $estado->save();
        $estado = new Estados();
        $estado->estado = "Confirmado";
        $estado->estado_id = "2";
        $estado->save();
        $estado = new Estados();
        $estado->estado = "Declinado"; //Concluido
        $estado->estado_id = "3";
        $estado->save();
        $estado = new Estados();
        $estado->estado = "Habilitado";
        $estado->estado_id = "4";
        $estado->save();
        $estado = new Estados();
        $estado->estado = "Deshabilitado";
        $estado->estado_id = "5";
        $estado->save();
        $estado = new Estados();
        $estado->estado = "Finalizado";
        $estado->estado_id = "6";
        $estado->save();
    }
}