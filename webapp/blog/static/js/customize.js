$("#post_comment").on("submit", function (e) {
    var post_id = document.getElementById("post_id").innerText
    var author = $(this).children().find("#name").val()
    var content = $(this).children().find("#message").val()
    console.log(author)
    console.log(content)
    var dataString = '{ "post_id":"'+post_id+'",'+
                        '"author":"'+author+'",'+
                        '"content":"'+content+'"'+
                      '}'
    console.log(dataString)

    $.ajax({
      type: "POST",
      url: "/blog/post_comment",
      contentType: 'application/json',
      data: dataString,
      success: function () {
        $('.comment-list').append(
            '<li class="comment">'+
                '<div class="vcard bio">'+
                    '<img src="/static/images/person_1.jpg" alt="Image placeholder">'+
                '</div>'+
                '<div class="comment-body">'+
                    '<h3>'+author+'</h3>'+
                    '<div class="meta mb-3">'+getNow()+'</div>'+
                    '<p>'+content+'</p>'+
                    '<p><a href="#" class="reply">Reply</a></p>'+
                '</div>'+
            '</li>');
      }
    });

    e.preventDefault();
});


$(function () {
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
});


function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }

function getNow() {
    var d = new Date();

    var month = Intl.DateTimeFormat('en-US', {month: 'long'}).format(d).slice(0,3);
    var date = d.getUTCDate();
    var year = d.getUTCFullYear();
    var hour = d.getUTCHours();
    var am_pm = ""
    if (hour == 12) {
        am_pm = "P.M.";
    } else if (hour > 12) {
        am_pm = "P.M.";
        hour = hour - 12;
    } else {
        am_pm = "A.M."
    }
    var min = d.getUTCMinutes();
    if (min < 9) {
        min = "0" + min;
    }

    render_date = month + ". " + date + ", " + year + ", " + hour + ":" + min + " " + am_pm;
    return render_date
}

var reply_state = false;

$(".reply").on("click", function (e) {
    if ($("#comment-popup").length) {
        if($(this).closest("ul div.comment-popup")) {
            alert("yes")
        }
//        $("#comment-popup").hide();
    } else {
        $(e.target).closest("ul").append(
        '<div id="comment-popup" class="comment-form-wrap pt-5">'+
            '<h3 class="mb-5">Leave a comment</h3>'+
            '<form id="post-comment" action="" class="p-5 bg-light">'+
                '<div class="form-group">'+
                    '<label for="name">Name *</label>'+
                    '<input type="text" class="form-control" id="name" required>'+
                '</div>'+
                '<div class="form-group">'+
                    '<label for="message">Message *</label>'+
                    '<textarea name="" id="message" cols="30" rows="10" class="form-control" required></textarea>'+
                '</div>'+
                '<div class="form-group">'+
                    '<input type="submit" value="Post Comment" class="btn py-3 px-4 btn-primary">'+
                '</div>'+
            '</form>'+
        '</div>');
    }
        e.preventDefault();
    });