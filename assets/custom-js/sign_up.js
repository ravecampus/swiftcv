$(function(){
    $('#signup_btn').on('click', function(e){
        e.preventDefault();
        $err = $('.error');

        $err.html('');
        $err.removeClass('errd');

        var this_ = $(this).closest('form');
        var form = this_.serialize();

         $.post('/member/',form).done(function(){
                window.location.href="/CV/";
         }).fail(function(err){
            var error = $.parseJSON(err.responseText)
            $.each(error, function(fields, messages){
                var field = fields.split('*')[0];
                var message = messages.split('*')[1];
                $('input[name='+field+']').prev('.error').html(message);
                $err.addClass('errd');
            });
         });
    });
});

$(function(){
    $('#btn-login').on('click', function(e){
        e.preventDefault();
        $err = $('.error_login');

        $err.html('');
        $err.removeClass('errd');

        var this_ = $(this).closest('form');
        var form = this_.serialize();

        $.post('/member/', form).done(function(){
            window.location.href="/CV/";
        }).fail(function(err){
            var error = $.parseJSON(err.responseText);
            $.each(error, function(fields, messages){
                var message = messages.split('*')[1];
                $err.html(message);
                $err.addClass('errd');
            });
        });
    });
});
