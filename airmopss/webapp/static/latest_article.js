$(function() {
    console.log($("#event-container"));

    function maFonction() {
        var event = $(this).data('event');
        event = JSON.parse(event.replace(/'/g, '"'));

        who = event.Who;
        what = event.What.answer;
        where = event.Where.answer;
        when = event.When.answer;

        $('#who').text(who);
        $('#what').text(what);
        $('#where').text(where);
        $('#when').text(when);
    }
    $(".tooltip").click(maFonction);
});

