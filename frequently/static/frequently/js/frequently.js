function openAnswer(answerID) {
    if ($('.answerID' + answerID).length == 0) {
        $.post(
            '.',
            {
                "csrfmiddlewaretoken": getCSRFToken(),
                "get_answer": answerID
            },
            function(data) {
                $(data).insertAfter('#frequentlyEntry' + answerID);
                initializeForm();
            }
        );
    }
}

function hideAnswer(answerID) {
    $('.answerID' + answerID).remove();
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

function initializeForm() {
    $('.frequentlyForm input[type="submit"]').click(function() {
        var form = $(this).closest('.frequentlyForm');
        var data = form.serializeArray();
        data.push({ name: this.name, value: this.value });
        form.find('input[type="submit"]').attr('disabled', true);
        $.post('.', data, function(data) {
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
}

function refreshRating(ratingID) {
    $.post(
        '.',
        {
            "csrfmiddlewaretoken": getCSRFToken(),
            "ratingID": ratingID
        },
        function(data) {
            $('.' + ratingID).html(data);
        }
    );
}