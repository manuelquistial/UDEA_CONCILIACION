<?php

namespace App;

use Illuminate\Database\Eloquent\Model;
use App\Usuario;

class Roles extends Model
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'tr_roles';

    /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = [
        'id', 'role', 'role_id', 'habilitador'
    ];

    public function usuario(){
        return $this->belongsToMany(Usuario::class, 'tr_usuarios_roles', 'role_id', 'usuario_id', 'role_id', 'id');
    }

    public function usuarioByRole($role_id){
        return $this->usuario()
                ->orWherePivot('role_id', '=', $role_id)
                ->where('tr_usuarios.estado_id', '=', 4);
    }
}
