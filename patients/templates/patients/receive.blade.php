@extends('template.layout')
@section('title'){{ __('appointments.appointment_booking') }}@endsection
@push('css')
@endpush
@section('content')
@if(Session::has('error'))
<p class="alert alert-danger">{{ Session::get('error') }}</p>
@endif
<div class="row">
    <div class="col-md-12 ">
        <div class="portlet box blue">
            <div class="portlet-title">
                <div class="caption">
                    <i class="fa fa-gift"></i> {{ __('appointments.appointment_booking') }}</div>
                <div class="tools">
                    <a href="javascript:;" class="collapse"> </a>
                </div>
            </div>
            <div class="portlet-body form">
                <div class="form-body">
                    <div class="form-group">
                        <form action="{{ route('appointments.patient.store')}}" method="post" class="mt-repeater horizontal-form" >
                        {{ csrf_field() }}
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="form-group form-group{{ $errors->has('user_id') ? ' has-error' : '' }}" >
                                        <label class="control-label">{{ __('doctors.doctor_name') }}  <span style="color: red">*</span> </label>
                                                 
                                        <select name="user_id"  required id="doctors" class="form-control action">
                                                <option value=""> {{ __('doctors.select_doctor') }}</option>
                                            @foreach($users  as $item)
                                                <option data-id="{{ $item->id}}" value="{{ $item->id }}"> {{$item->name}} </option>
                                            @endforeach
                                        </select>
                                        <input type="text" hidden name="patient_id" value="{{ Request::segment(3) }}">
                                        @if ($errors->has('user_id'))
                                        <div class="alert alert-danger alert-dismissible fade in" role="alert">
                                        {{ $errors->first('user_id') }}
                                        </div>
                                        @endif
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="form-group form-group{{ $errors->has('appdata') ? ' has-error' : '' }}" >
                                        <label class="control-label"> {{ __('appointments.appdata') }}  :  <span style="color: red">*</span></label>
                                        <input class="form-control action" value="{{ old('appdata') }}"  name="appdata" id="appdata" type="date"/>
                                        @if ($errors->has('appdata'))
                                        <div  role="alert">
                                        <span style="color: red;">{{ $errors->first('appdata') }}</span>
                                        </div>
                                        @endif
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                  <div class="col-md-12">
                                    <div class="form-group form-group{{ $errors->has('price') ? ' has-error' : '' }}" >
                                        <label class="control-label"> {{ __('appointments.price') }}  :  </label>
                                        <input class="form-control action" value="{{ old('price') }}"  name="price"  type="number"/>
                                        @if ($errors->has('price'))
                                        <div  role="alert">
                                        <span style="color: red;">{{ $errors->first('price') }}</span>
                                        </div>
                                        @endif
                                    </div>
                                </div>
                                
                            </div>
                            <table class="table table-bordered">
                                <thead style="background-color: #F5F5F5">
                                  <tr>
                                    <th scope="col">#</th>
                                    <th scope="col">{{ __('site.patient_name') }}</th>
                                  </tr>
                                </thead>
                                <tbody id="mytable">
                                </tbody>
                              </table>
                       <div class="form-actions right">
                              <button type="submit" class="btn blue" id="add_btn">
                                  <i class="fa fa-check"></i> {{ __('site.booking') }}</button>
                          </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div> 
</div>

@push('js')
<script type="text/javascript">
    //we store out timerIdhere
var timeOutId = 0;
    $(".action").change(function (e) {
        e.preventDefault();
        var doctor = $('#doctors').val();
        var appdata = $('#appdata').val();
        $.ajax({
            url: "{{ route('appointments.get_doctor') }}",
            method: "post",
            data: {_token: '{{ csrf_token() }}',
            doctor: doctor,
            appdata:appdata
            },
            beforeSend: function() {
                $('.action').prop('disabled', true);
            },
            success: function (response) {
                var trHTML = '';
                var inc = 1;
                $.each(response.data, function (i, item) {
                 trHTML += '<tr><td>' + inc++ +
                    '</td><td>' + item.patients.title +
                    '</td></tr>'; 
                 });
                $('#mytable').html(trHTML);
                $('.action').prop('disabled', false);
            }
            
        });
     });
    
    </script>
@endpush
@endsection



    







