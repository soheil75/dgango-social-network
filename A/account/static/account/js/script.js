$(function () {
    $(".action-btn").on("click", function () {
        let type = $(this).attr('data-type')
        let data = $(this).attr('data-id')
        sendData(type, data)
    });
});
function sendData(type, data) {
    //-------------------------------------
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    //--------------------------------------------
    let path = "/account/" + type + "/"
    $.ajax({
        method: 'POST',
        url: path,
        data: {
            'user-id': data,
        },
        success: function (response) {
            console.log(response)
            if (response['status'] == 'ok') {
                if (type == 'follow') {
                    $(".action-btn")
                        .attr('data-type', 'unfollow')
                        .removeClass('btn-primary')
                        .addClass('btn-light')
                        .text('Unfollow');
                } else {
                    $(".action-btn")
                        .attr('data-type', 'follow')
                        .removeClass('btn-light')
                        .addClass('btn-primary')
                        .text('Follow');
                }
            }
        },
        error: function (error) {
            console.log(error)
        }
    });
}