<?php

namespace App\Http\Controllers;

use Auth;
use File;
use Illuminate\Support\Facades\DB;
use Illuminate\Http\Request;
use Symfony\Component\Process\Process;
use Symfony\Component\Process\Exception\ProcessFailedException;

class UploadFileController extends Controller
{
    /**
     * Create a new controller instance.
     *
     * @return void
     */
    public function __construct()
    {
      $this->middleware('auth');
    }

    /**
     * Show the upload file view
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
      return view('upload_file');
    }

    /**
     * Download the reservas files
     *
     * @param Request $request
     * @return \Illuminate\Http\JsonResponse
     */
    public function downloadReservas(Request $request)
    {
      // validate user input
      $request->validate([
          'num' => 'required',
      ]);
      // get user id and value from request
      $userId = Auth::id();
      $value = request()->num;
      // find the necessary files in the storage directory
      $files = glob(storage_path('app/public/files/reservas')."/*".$value."_".$userId.".{xlsx,XLSX}", GLOB_BRACE);
      if(empty($files) || (count($files) != 2)){
          // return error if files are not found or not valid
          return response()->json(['empty'=>'No existen los documentos necesarios para realizar reservas', 'files'=>json_encode($files)]);
      }else{
          // run the python script with the necessary arguments
          $process = new Process("python3 ".storage_path('app/public')."/reservas.py ".$value." ".$files[0]." ".$files[1]." ".storage_path('app/public/files/')." ".$userId);
          try {
              $process->mustRun();
              //delete the original files
              FILE::delete($files);
              $data = glob(storage_path('app/public/files/').'files_out/*'.$value."_".$userId.'.xlsx');
              return json_encode($data);
          } catch (ProcessFailedException $exception) {
              return response()->json(['error'=>$exception->getMessage()]);
          }
      }
    }

    /**
      * Download the conciliacion files
      *
      * @param Request $request
      * @return \Illuminate\Http\JsonResponse
      */
    public function downloadConciliacion(Request $request)
    {
      //validate user input
      $request->validate([
      'num' => 'required',
      ]);
      //get user id and values from the database
      $userId = Auth::id();
      $porcentajes = DB::table('cn_porcentajes')->get();
      $salud = $porcentajes[0]->porcentaje_salud;
      $ingresos = $porcentajes[0]->porcentaje_ingresos;
      $value = request()->num;
      //find the necessary files in the storage directory
      $files = glob(storage_path('app/public/files/conciliacion')."/*".$value."_".$userId.".{xlsx,XLSX}", GLOB_BRACE);
      if(empty($files) || (count($files) < 2)){
        //return error if files are not found or not valid
        return response()->json(['empty'=>'No existen los documentos necesarios para conciliar', 'files'=>json_encode($files)]);
      }else{
        //run the python script with the necessary arguments
        $process = new Process("python3 ".storage_path('app/public')."/conciliacion.py ".$value." ".storage_path('app/public/files/')." ".$userId." ".$salud." ".$ingresos);
        try {
          $process->mustRun();
          //delete the original files
          FILE::delete($files);
          $data = glob(storage_path('app/public/files/').'files_out/*'.$value."_".$userId.'.xlsx');
          return json_encode($data);
        } catch (ProcessFailedException $exception) {
          return response()->json(['error'=>$exception->getMessage()]);
        }
      }
    }

    /**
     * Download the conciliacion result file
     *
     * @param Request $request
     * @return \Illuminate\Http\Response
     */
    public function download(Request $request)
    {
      //get user id and file name from request
      $userId = Auth::id();
      $request->validate([
          'name' => 'required',
      ]);
      $name = request()->name;
      $file = storage_path('app/public/files/files_out/').$name;
      //modify the file name
      $name = explode("_", request()->name);
      array_pop($name);
      // download the file and delete it after sending it
      return response()->download($file, implode("_", $name).".xlsx")->deleteFileAfterSend(true);
    }

    /**
      * Handles the file upload and checks for the correct file type
      *
      * @param Request $request
      * @return \Illuminate\Http\JsonResponse
      */
    public function fileUploadPost(Request $request)
    {
      //validate user input
      $request->validate([
        'file' => 'required',
      ]);

      // get user id and file name
      $userId = Auth::id();
      $fileName = strtolower(request()->file->getClientOriginalName());
      // remove file extension
      $fileName = str_replace(".xlsx","",$fileName);
      // append user id to file name
      $fileName = $fileName."_".$userId.".xlsx";
      $var = strtolower($fileName);
      // check if file name contains the correct keywords and move file to the appropriate directory
      if((strpos($var, "reservas") !== false) & ((strpos($var, "sap") !== false) || (strpos($var, "sigep") !== false))){
        request()->file->move(storage_path('app/public/files/reservas'), $fileName);
        return response()->json(['success'=>'Archivo agregado']);
      }elseif((strpos($var, "pagos") !== false) || (strpos($var, "recaudos") !== false) || (strpos($var, "general") !== false)){
        request()->file->move(storage_path('app/public/files/conciliacion'), $fileName);
        return response()->json(['success'=>'Archivo agregado']);
      }else{
        return response()->json(['error'=>'Archivo incorrecto']);
      }
  }
}
