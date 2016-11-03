$(function(){
    $('#btn_work').on('click', function(){

      var csrf = $('input[name=csrfmiddlewaretoken]').val();
      var id = $('input[name=section-id]').val();
      $educ = $('#work');
      
      var form = new FormData();                        
      form.append('csrfmiddlewaretoken', csrf); 

        $.ajax({
            url: '/CV/work/'+id+'/',
            dataType: 'script',
            cache: false,
            contentType: false,
            processData: false,
            data: form,   
            type: 'post'
       }).done(function(){
            loadWork(); 
       }); 
     
  });

    $work = $('#work_set');
    $work.sortable();
    $work.disableSelection();
    $work.css({'cursor':'move'});
});

var loadWork = function(){
   var id = $('input[name=section-id]').val();
  return  $.get('/CV/work/load/'+id+'/').done(function(data){
      $('#work_set').html(data);

    });
}

loadWork();

$(function(){
  $('#work_set').on('click','.btn-work', function(){
      $this = $(this);
      var id = $this.parent('#work').data('work-id');

      $.get('/CV/work/del/'+id+'/').done(function(){
           $this.parent('#work').remove();
      });
  });
});

// navigation sorting
$(function() {
    $nav = $("#sortable");
    $nav.sortable();
    $nav.disableSelection();
    $nav.css({'cursor':'move'});
});



 // var work = (
 //        '<div id="work">'+
 //          '<div class="col-md-12">'+
 //             '<div class="col-md-6">'+
 //                  '<div class="form-group">'+
 //                    '<label>Job title</label>'+
 //                    '<input type="text" name="job_title" class="form-control text-cv">'+
 //                  '</div>'+
 //                 '<div class="form-group">'+
 //                    '<label>Start date</label>'+
 //                    '<input type="text" name="start_date_w" class="form-control text-cv">'+
 //                  '</div>'+
 //              '</div>'+
 //              '<div class="col-md-6">'+
 //                '<div class="form-group">'+
 //                    '<label>Company name</label>'+
 //                    '<input type="text" name="company_name" class="form-control text-cv">'+
 //                  '</div>'+
 //                 '<div class="form-group">'+
 //                    '<label>End date</label>'+
 //                    '<input type="text" name="end_date_w" class="form-control text-cv">'+
 //                  '</div>'+
 //              '</div>'+
 //           '</div>'+
 //           '<hr class="line-style">'+
 //           '<div class="col-md-12">'+
 //               '<div class="col-md-12">'+
 //                '<label>Other Information</label>'+
 //                '<textarea name="other_information_w" class="form-control text-cv"></textarea>'+
 //                '<p>Optional details such as job responsibilities, achievements etc.</p>'+
 //               '</div>'+
 //          '</div>'+ 
 //          '<button class="btn btn-cv btn-delete btn-work ">Delete</button>'+
 //          '<hr class="line-style">'+
 //        '</div>');

 //        var divs = $('#work_set');
 //        // $div.removeClass('hide');
 //        divs.append(work);
 //        tinymce.init({ 
 //            selector:'textarea',
 //        }); 