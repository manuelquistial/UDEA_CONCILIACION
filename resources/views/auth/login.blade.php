@extends('layouts.app')

@section('content')
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header">{{ Lang::get('strings.login.iniciar_sesion') }}</div>

                <div class="card-body">
                    <form class="form-horizontal" method="POST" action="{{ route('login') }}">
                        {{ csrf_field() }}

                        <div class="form-group{{ $errors->has('usuario') ? ' has-error' : '' }}">
                            <label for="usuario" class="control-label">{{ Lang::get('strings.login.usuario') }}</label>

                            <input id="usuario" type="string" class="form-control" name="usuario" value="{{ old('usuario') }}" required autofocus>

                            @if ($errors->has('usuario'))
                                <span class="text-danger">
                                    <strong><small>{{ $errors->first('usuario') }}</small></strong>
                                </span>
                            @endif
                        </div>

                        <div class="form-group{{ $errors->has('password') ? ' has-error' : '' }}">
                            <label for="password" class="control-label">{{ Lang::get('strings.login.password') }}</label>

                            <input id="password" type="password" class="form-control" name="password" required>

                            @if ($errors->has('password'))
                                <span class="text-danger">
                                    <strong><small>{{ $errors->first('password') }}</small></strong>
                                </span>
                            @endif
                        </div>

                        <div class="form-group">
                            <button type="submit" class="btn btn-primary">
                            {{ Lang::get('strings.login.conectar') }}
                            </button>

                            <a class="btn btn-link" href="{{ route('password.request') }}">
                            {{ Lang::get('strings.login.olvido_password') }}
                            </a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
@endsection
