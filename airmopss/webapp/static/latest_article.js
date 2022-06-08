$(function() {
    console.log($("#event-container"));

    function maFonction() {
        var event = $(this).data('event');
        $('#event-container').text(event);
    }
    $(".tooltip").click(maFonction);


    console.log('LOADED2');
    console.log('LOADED2');
});

