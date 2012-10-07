function openAnswer(answerID) {
    $('.answerID' + answerID).slideDown();
    $.post(
        '',
        {
            "csrfmiddlewaretoken": getCSRFToken(),
            "refresh_last_view": answerID
        },
        function(data) {
            alert(data);
        }
    );
}

function hideAnswer(answerID) {
    $('.answerID' + answerID).slideUp();
}

function getCSRFToken() {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, 10) == ('csrftoken' + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    return cookieValue;
}

function refreshRating(ratingID) {
    $.post(
        '',
        {
            "csrfmiddlewaretoken": getCSRFToken(),
            "ratingID": ratingID
        },
        function(data) {
            $('.' + ratingID).html(data);
        }
    );
}

$(document).ready(function() {
    $('.frequentlyAnswer').slideUp();

    $('.frequentlyForm input[type="submit"]').click(function() {
        var form = $(this).closest('.frequentlyForm');
        var data = form.serializeArray();
        data.push({ name: this.name, value: this.value });
        form.find('input[type="submit"]').attr('disabled', true);
        $.post('', data, function(data) {
            form.find('input[type="submit"]').remove();
            refreshRating(form.attr('id'));
            form.prepend(data).find('.sendFeedback').click(function() {
                data = form.serializeArray();
                data.push({ name: this.name, value: this.value });
                $.post('', data, function(data) {
                    form.find('.feedbackForm').remove();
                    form.prepend(data);
                });
                return false;
            });
        });
        return false;
    });
});