$(function(){
    $('#btn-special-section').on('click', function(){
        var id = $(this).data('id');
        $('.cv-special-section').modal('show');
        $('input[name=section_id]').val(id);
    });

   
    $('#btn-add-special-section').on('click', function(){
        $form = $('#form-special-section');
        $id = $('input[name=section_id]').val();
        $.post('/CV/special_section/'+$id+'/', $form.serialize()).done(function(){
            window.location.href = '/CV/'+$id+'/';
        });
    });
   
});

$(function(){
    $('.btn-delete-special').on('click', function(){
        // console.log('hello');
        $this = $(this);
        var id = $this.data('sp-id');
        var section_id = $this.data('sec-id');
        $('input[name=special_id]').val(id);
        $('.special-section-del').modal('show');
        $('input[name=section_id]').val(section_id);
    });
    $('#btn-delete-sp').on('click', function(){
        $id = $('input[name=section_id]').val();
        $sp_id = $('input[name=special_id]').val();
        console.log($sp_id)
        $.get('/CV/special_section/del/'+$sp_id+'/').done(function(){
             window.location.href = '/CV/'+$id+'/';
        });
    });
    
});


$(function(){
    $('.link-edit-section').on('click', function(){
        $('.edit-section').modal('show'); 
        $('input[name=sp-id]').val($(this).data('sp-id'));
        $('#sp-text').val($(this).data('name'));
    });

    $('#btn-edit-section').on('click', function(){
         var form = $('#form-edit-section').serialize();

         // $.post()
    });
});