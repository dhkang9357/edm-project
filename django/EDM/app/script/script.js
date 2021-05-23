function on_button_click()
{
    //alert('hello');

    $.get('/get_map_data', function(map_data) {
        $('#div_map').html(map_data);
    })
}