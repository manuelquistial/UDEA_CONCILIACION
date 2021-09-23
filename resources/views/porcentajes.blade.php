@extends('layouts.app')

@section('porcentajes')
    <a class="nav-link active" href="{{ route('list_porcentajes') }}">{{ __('Porcentajes') }}</a>
@endsection

@section('content')
    @if (session('status'))
        <div class="alert alert-danger" role="alert">
            {{ session('status') }}
        </div>
    @endif
    <div class="row justify-content-center">
        <div class="card col-sm-6" style="padding: 0px">
            <div class="card-header">
              Porcentajes
            </div>
            <div class="card-body">
                <form action="{{ route('update_porcentajes') }}" method="post"  enctype="multipart/form-data">
                    {!! csrf_field() !!}
                    <input type="text" name="code" value="{{ $code }}" hidden>
                    <div class="form-group row">
                      <label for="salud" class="col-sm-2 col-form-label">Salud</label>
                      <div class="col-sm-10">
                        <input type="text" class="form-control" id="salud" name="salud" placeholder="Salud" value="{{ $salud != '' ? $salud : '' }}">
                      </div>
                    </div>
                    <div class="form-group row">
                        <label for="salud" class="col-sm-2 col-form-label">Ingresos</label>
                        <div class="col-sm-10">
                          <input type="text" class="form-control" id="ingresos" name="ingresos" placeholder="Ingresos" value="{{ $ingresos != '' ? $ingresos : '' }}">
                        </div>
                      </div>
                    <div class="form-group row">
                        <div class="col-sm-10">
                            <button type="submit" class="btn btn-primary">Guardar</button>
                        </div>
                    </div>
                </form>
            </div>
          </div>
    </div>
@endsection
