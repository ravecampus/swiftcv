
$(function(){
    $('#btn_education').on('click', function(){
      var csrf = $('input[name=csrfmiddlewaretoken]').val();
      var id = $('input[name=section-id]').val();
      $educ = $('#education');
      

      var form = new FormData();                        
      form.append('csrfmiddlewaretoken', csrf); 

        $.ajax({
            url: '/CV/education/'+id+'/',
            dataType: 'script',
            cache: false,
            contentType: false,
            processData: false,
            data: form,   
            type: 'post'
       }).done(function(){
            loadView(); 
       }); 
    });

    $edu = $('#education_set');
    $edu.sortable();
    $edu.disableSelection();
    $edu.css({'cursor':'move'});
   
});

var loadView = function(){
   var id = $('input[name=section-id]').val();
  return  $.get('/CV/education/load/'+id+'/').done(function(data){
      $('#education_set').html(data);

    });
}

loadView();

// delete education form
$(function(){
  $('#education_set').on('click','.btn-delete', function(){
      $this = $(this);
      var id = $this.parent('#education').data('edu-id');

      $.get('/CV/education/del/'+id+'/').done(function(){
           $this.parent('#education').remove();
      });
  });
});







 // tinymce.init({ 
 //            selector:'textarea',
 //        }); 

// var education = function(id){

//   var education_content = (
//     '<div id="education" data-edu-id="'+id+'">'+
//       '<div class="col-md-12">'+
//          '<div class="col-md-6">'+
//               '<div class="form-group">'+
//                 '<label>Course name</label>'+
//                 '<input type="text" name="course" class="form-control text-cv">'+
//               '</div>'+
//              '<div class="form-group">'+
//                 '<label>Start date</label>'+
//                 '<input type="text" name="start_date_e" class="form-control text-cv">'+
//               '</div>'+
//           '</div>'+
//           '<div class="col-md-6">'+
//             '<div class="form-group">'+
//                 '<label>Institution name</label>'+
//                 '<input type="text" name="institution" class="form-control text-cv">'+
//               '</div>'+
//              '<div class="form-group">'+
//                 '<label>End date</label>'+
//                 '<input type="text" name="end_date_e" class="form-control text-cv">'+
//               '</div>'+
//           '</div>'+
//      '</div>'+
//      '<hr class="line-style">'+
//      '<div class="col-md-12">'+
//          '<div class="col-md-12">'+
//           '<label>Other Information</label>'+
//           '<textarea name="information" class="form-control text-cv"></textarea>'+
//           '<p>Optional details such as course description, marks etc.</p>'+
//          '</div>'+
//     '</div>'+ 
//     '<button class="btn btn-cv btn-delete">Delete</button>'+
//     '<hr class="line-style">'+
// '</div>');
//        // var edu_= $('#education');

//         var divs = $('#education_set');
//         // $div.removeClass('hide');
//      return   divs.append(education_content);

// }

// for(i=0; i < 5; i++){
// education();
// }