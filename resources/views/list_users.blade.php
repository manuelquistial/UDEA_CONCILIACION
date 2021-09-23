@extends('layouts.app')

@section('lista_usuarios')
    <a class="nav-link active" href="{{ route('list_users') }}">{{ __('Lista Usuarios') }}</a>
@endsection

@section('content')
    @if (session('status'))
        <div class="alert alert-danger" role="alert">
            {{ session('status') }}
        </div>
    @endif
    <div class="row justify-content-center">
        <div class="card col-sm-8" style="padding: 0px">
            <div class="card-header">
              Usuarios
            </div>
            <div class="card-body">
                <table class="table">
                    <thead>
                        <tr>
                        <th scope="col">{{ __('Nombre') }}</th>
                        <th scope="col">{{ __('Email') }}</th>
                        <th scope="col"></th>
                        </tr>
                    </thead>
                    <tbody>
                    @foreach ($users as $user)
                        <tr>
                            <td>{{ $user->nombre_apellido }}</td>
                            <td>{{ $user->email }}</td>
                        </tr>
                    @endforeach
                    </tbody>
                </table>
            </div>
        </div>
    </div>
@endsection
