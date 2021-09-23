<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Porcentajes extends Model
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'cn_porcentajes';

    /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = [
        'id', 'porcentaje_salud', 'porcentaje_ingresos'
    ];
}
