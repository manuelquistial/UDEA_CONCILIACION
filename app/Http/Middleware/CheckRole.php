<?php

namespace App\Http\Middleware;

use Closure;

class CheckRole
{
    /**
     * Handle an incoming request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @return mixed
     */
    public function handle($request, Closure $next, $role){
        if(\Auth::check() && $request->user()->hasOneRole($role) != null){
            if (!$request->user()->hasOneRole($role)) {
    
                return redirect('/');
            }
    
            return $next($request);
        }
        return redirect('/');
    }
}
