$( document ).on('click', '#create_token', function(event) {
    //console.log('Step 1');
    $.ajax({
                url: '/users/create_token/',
                success: function (data) {
                    //console.log('Step 3')
                    //console.log(data.key);
                    $('#token').html(data.key);
                    $('#token').html(data.key);
                },
            });
});