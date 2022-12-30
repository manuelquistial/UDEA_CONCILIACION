<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Estados extends Model
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'tr_estados';

    /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = [
        'id', 'estado', 'estado_id'
    ];
}