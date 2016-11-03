$(function(){
    $('#btn-upload').on('click', function(){
        $form = $('#cvform');
        var csrf = $('input[name=csrfmiddlewaretoken]').val();
        $photo = $("#photo").prop('files')[0]
        var id = $('input[name=section-id]').val();

        var form_data = new FormData();                        
        form_data.append('csrfmiddlewaretoken', csrf); 
        form_data.append('photo', $photo);        
      
        
        $.ajax({
            url: '/CV/photo/'+id+'/',
            dataType: 'script',
            cache: false,
            contentType: false,
            processData: false,
            data: form_data,   
            type: 'post'
       }).done(function(){
            if($photo){
                var reader = new FileReader();
                reader.onload = function(e){
                    $('.profile-pic').attr('src', e.target.result);
                }
                reader.readAsDataURL($photo)
                $('#photo').val('');
            }
       });
 
    });
});

$(function(){
    $('#photo-remove').on('click', function(){

        var id = $('input[name=section-id]').val();       
        var csrf = $('input[name=csrfmiddlewaretoken]').val();

        var form = new FormData();
            form.append('csrfmiddlewaretoken', csrf);

            $.ajax({
                url:'/CV/photo/del/'+id+'/',
                dataType:'script',
                cache: false,
                contentType:false,
                processData: false,
                data: form,
                type: 'post',
            }).done(function(){
                $('.profile-pic').attr('src', '');
            });


    });
});