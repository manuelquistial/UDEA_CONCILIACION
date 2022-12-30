<?php

use Illuminate\Database\Seeder;
use App\Roles;

class RolesSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        $role = new Roles();
        $role->role = "Administrador";
        $role->role_id = "1";
        $role->habilitador = True;
        $role->save();
    }
}