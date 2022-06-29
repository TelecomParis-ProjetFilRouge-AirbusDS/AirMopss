$(function() {
    console.log($("#event-container"));

    function maFonction() {
        var event_start_idx = $(this).data('start-idx');
        var event_end_idx = $(this).data('end-idx');
        var event = $(this).data('event');

        console.log(event);

        who = event.Who;
        what = event.What.answer;
        where = event.Where.answer;
        when = event.When.answer;

        $('#who').text(who);
        $('#what').text(what);
        $('#where').text(where);
        $('#when').text(when);

        [$("#event-label-good"), $("#event-label-bad")].forEach(function(element) {
            element.data('start-idx', event_start_idx);
            element.data('end-idx', event_end_idx);
            element.data('event', event);
        });
    }
    $(".event").click(maFonction);

    function labelEvent() {
        var article_id = $(".article").data('article-id');
        var event_start_idx = $(this).data('start-idx');
        var event_end_idx = $(this).data('end-idx');
        var event = $(this).data('event');
        var label;

        if ($(this).attr('id') == 'event-label-good') {
            label = 1;
        } else {
            label = 0;
        }

        labeled_event_data = {
            article_id: article_id,
            event_start_idx: event_start_idx,
            event_end_idx: event_end_idx,
            event: event,
            label: label
        }

        console.log(labeled_event_data);

        $.ajax({
            type: "POST",
            url: "/labels",
            data: JSON.stringify(labeled_event_data),
            contentType: "application/json",
            dataType: 'json',
            success: function(data, _, _) {
                console.log(data);
            }
        });
    }
    $("#event-label-good").click(labelEvent);
    $("#event-label-bad").click(labelEvent);
});

