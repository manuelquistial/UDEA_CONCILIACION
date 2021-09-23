<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Porcentajes;

class PorcentajeController extends Controller
{
    public function __construct(){
        $this->middleware('auth');
    }

    /**
     * Show the application dashboard.
     *
     * @return \Illuminate\Http\Response
     */

    public function index(){
        $porcentajes = Porcentajes::select('id', 'porcentaje_salud', 'porcentaje_ingresos')->first();
        $code = '';
        $salud = '';
        $ingresos = '';

        if(isset($porcentajes->id)){
            $code = $porcentajes->id;
        }

        if(isset($porcentajes->porcentaje_salud)){
            $salud = $porcentajes->porcentaje_salud;
        }

        if(isset($porcentajes->porcentaje_ingresos)){
            $ingresos = $porcentajes->porcentaje_ingresos;
        }

        return view('porcentajes', compact('salud', 'ingresos', 'code'));
    }

    /**
     * Create a new user instance after a valid registration.
     *
     * @param  array  $data
     * @return \App\Legalizado
     */
    public function create(array $data)
    {
        $porcentajes = Porcentajes::create([
            'porcentaje_salud' => str_replace(',', '.', $data['salud'] ? $data['salud'] : '0'),
            'porcentaje_ingresos' => str_replace(',', '.', $data['ingresos'] ? $data['ingresos'] : '0')
        ]);

        return $porcentajes;
    }

    /**
     * Update porcentajes.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */

    public function update(Request $request){
        $code = $request->code;
        $data = $request->except('_token', 'code');
        $porcentaje = Porcentajes::where('id', $code)->first();

        if(isset($porcentaje->id)){
            Porcentajes::where('id', $code)
                    ->update([
                        'porcentaje_salud' => str_replace(',', '.', $data['salud'] ? $data['salud'] : '0'),
                        'porcentaje_ingresos' => str_replace(',', '.', $data['ingresos'] ? $data['ingresos'] : '0')
                    ]);
        }else{
            $store = $this->create($data);
            $store->save();
        }


        return redirect('porcentajes');
    }
}
