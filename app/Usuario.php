<?php

namespace App;

use Illuminate\Notifications\Notifiable;
use Illuminate\Foundation\Auth\User as Authenticatable;
use App\Notifications\PasswordReset;
use App\Roles;

class Usuario extends Authenticatable
{
    use Notifiable;

    protected $connection = 'mysql';

    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = 'tr_usuarios';

    /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = [
        'nombre_apellido', 'email', 'telefono', 'cedula', 'usuario', 'password', 'estado_id'
    ];

    /**
     * The attributes that should be hidden for arrays.
     *
     * @var array
     */
    protected $hidden = [
        'password', 'remember_token',
    ];

    public function role(){
        return $this->belongsToMany(Roles::class, 'tr_usuarios_roles', 'usuario_id', 'role_id');
    }

    /**
    * Check one role
    * @param string $role
    */
    public function hasOneRole($role){
        return null !== $this->role()->where('role', $role)->first();
    }

    /**
     * Send the password reset notification.
     *
     * @param  string  $token
     * @return void
     */
    public function sendPasswordResetNotification($token)
    {
        $this->notify(new PasswordReset($token));
    }
}
