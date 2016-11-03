
$(function(){
    $('#btn_cvform').on('click', function(){
        $save = $('.save');
        $save.html('Saving...');
        $save.addClass('process');

        var id = $('input[name=section-id]').val();
        $form = $('#cvform');
        $data = $form.serializeArray()
        
        $('input[name=course]').map(function(){
            $data.push(
                {name:'course', value:$(this).val()});
        });
        $('input[name=institution]').map(function(){
            $data.push(
                {name:'institution', value:$(this).val()});
        });
        $('input[name=end_date_e]').map(function(){
            $data.push(
                {name:'end_date', value:$(this).val()});
        });

        $('input[name=start_date_e]').map(function(){
            $data.push(
                {name:'start_date', value:$(this).val()});
        });

        $('textarea[name=information]').map(function(){
            $data.push(
                {name:'information', value:$(this).val()});
        });



         $('input[name=job_title]').map(function(){
            $data.push(
                {name:'job', value:$(this).val()});
        });
        $('input[name=company_name]').map(function(){
            $data.push(
                {name:'company', value:$(this).val()});
        });
        $('input[name=end_date_w]').map(function(){
            $data.push(
                {name:'end_date_work', value:$(this).val()});
        });

        $('input[name=start_date_w]').map(function(){
            $data.push(
                {name:'start_date_work', value:$(this).val()});
        });

        $('textarea[name=other_information_w]').map(function(){
            $data.push(
                {name:'other_information_work', value:$(this).val()});
        });

        $.post('/CV/'+id+'/',$data).done(function(){
            $save.html('Saved');
            setTimeout(function(){
                 $save.html('');
                 $save.removeClass('process');
            }, 2000);

        });
    });
});

$(function(){
    $('#btn-section').on('click', function(){
        $form = $('#form-section');

        $err = $('.error');
        $err.html('');
        $err.removeClass('errd');

        $.post('/CV/', $form.serialize()).done(function(success){
                  window.location.href="/CV/"+success;   
        }).fail(function(err){
            var error = $.parseJSON(err.responseText)
            $.each(error, function(fields, messages){
                var field = fields.split('*')[0];
                var message = messages.split('*')[1];
                
                $('#sec_'+field).prev('.error').html(message);
                $err.addClass('errd');
            });
        });
    })
});


$(function(){
    $('.btn-delete-sec').on('click', function(){
        var del = $(this).data('id');
        $('input[name=section-id]').val(del);
    });
    $('#btn-delete').on('click', function(){
        var val = $('input[name=section-id]').val();

        $.get('/CV/delete/'+val+'/').done(function(){
            window.location.href='/CV/';
        });
    });
});

$(function(){
    $('.btn-rename-cv').on('click', function(){
        var val = $(this).data('name');
        var id = $(this).data('id');

        $modal = $('.cv-rename');
        $modal.modal('show');
        $modal.parent().find('input[name=name]').val(val);
        $modal.parent().find('input[name=section-id]').val(id);

    });

    $('#btn_rename').on('click', function(){
        $form = $('#form-rename');
        $id = $('input[name=section-id]').val();

        $err = $('.error-rename-section');
        $err.html('');
        $err.removeClass('errd');

        $.post('/CV/rename/'+$id+'/', $form.serialize()).done(function(){
            window.location.href='/CV/';
        }).fail(function(err){
            var error = $.parseJSON(err.responseText)
            $.each(error, function(fields, messages){
                var field = fields.split('*')[0];
                var message = messages.split('*')[1];
                $('#re_'+field).prev('.error-rename-section').html(message);
                $err.addClass('errd');
            });

        });
    });
});


