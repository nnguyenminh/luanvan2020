$("#leaveCommentForm").on("submit", function (e) {
    var post_id = document.getElementById("post_id").innerText;
    var author = $(this).find("#name").val();
    var content = $(this).find("#message").val();
    var dataString = '{ "post_id":"' + post_id + '",' +
        '"author":"' + standardize_request(author) + '",' +
        '"content":"' + standardize_request(content) + '"' +
        '}';

    $.ajax({
        type: "POST",
        url: "/blog/post_comment",
        contentType: 'application/json',
        data: dataString,
        success: function (dataserver) {
            var x = document.getElementById('commentList').innerHTML;
            var comment = "<li class='comment'><p id='comment_id' hidden>" + dataserver.id + "</p><div class='vcard bio'><img src='/static/images/person_1.jpg' alt='Image placeholder'></div><div class='comment-body'><h3>" + dataserver.author + "</h3><div class='meta mb-3'>" + format_date(dataserver.created_at) + "</div><p>" + dataserver.content + "</p><a class='replycm'>Reply</a></div></li>";
            x = comment + x;
            document.getElementById("commentList").innerHTML = x;
            $('#leaveCommentForm #message').val('');
        }
    });


    e.preventDefault();
});

$(function () {
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
});


function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start, c_end));
        }
    }
    return "";
}

function getNow() {
    var d = new Date();

    var month = Intl.DateTimeFormat('en-US', { month: 'long' }).format(d).slice(0, 3);
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

$(document).ready(function () {
    $(document).on("click", "a.replycm", function (e) {
        $("#replyCommentForm").remove();
        $(this).parent().append(
            '<form id="replyCommentForm" style="margin-top: 15px;"><div class="form-group"><div class="row" style="margin-bottom: 10px;margin-left: 0;margin-right: 0;"><div class="col" style="padding: 0;"><input type="text" class="form-control" placeholder="Your name"></div></div><textarea type="text" class="form-control" id="formGroupExampleInput2" placeholder="Write here.." style="margin-bottom: 10px;"></textarea><button type="button" class="btn btn-primary replycm">Comment</button><button class="btn btn-cancel">Cancel</button></div></form>'
        );
        e.preventDefault();
    })

    $(document).on('click', '#replyCommentForm button.btn-cancel', function () {
        $("#replyCommentForm").remove();

    })

    $(document).on('click', 'button.replycm', function () {
        var post_id = document.getElementById("post_id").innerText;
        var parent_id = $("#replyCommentForm").parent().parent().find('#comment_id')[0].innerHTML;
        var author = $(this).parent().find('input').val()
        var content = $(this).parent().find('textarea').val();
        var dataString = '{ "post_id":"' + post_id + '",' +
            '"author":"' + standardize_request(author) + '",' +
            '"content":"' + standardize_request(content) + '",' +
            '"parent_id":"' + standardize_request(parent_id) + '"' +
            '}';

        root = $(this).closest(".root-comment")

        $.ajax({
            type: "POST",
            url: "/blog/post_comment",
            contentType: 'application/json',
            data: dataString,
            success: function (dataserver) {
                var li = "<li class='comment'><p id='comment_id' hidden>" + dataserver.id + "</p><div class='vcard bio'><img src='/static/images/person_1.jpg' alt='Image placeholder'></div><div class='comment-body'><h3>" + replace_quotes(dataserver.author) + "</h3><div class='meta mb-3'>" + format_date(dataserver.created_at) + "</div><p>" + replace_quotes(dataserver.content) + "</p><a class='replycm'>Reply</a></div></li>";
                root.find("ul.children").append(li);

                $("#replyCommentForm").remove();
            }
        });
    })
})

var data;

const preload_comments = (id) => {
    $.ajax("/blog/load_comments/post=" + id, {
        success: function (dataserver, status, xhr) {
            data = dataserver.reverse();
            loadComment();
        }
    })
}

// const load_recent_posts = (id) => {
//     $.ajax("/blog/load_comments/post=" + id, {
//         success: function (dataserver, status, xhr) {
//             data = dataserver.reverse();
//             loadComment();
//         }
//     })
// }

var start = 0;
var stop = 1;

var loadComment = () => {
    // alert(data.length);
    // var max = 1;
    // var len = document.getElementById('commentList').childElementCount;
    for (start; start < data.length; start++) {
        if (start <= stop) {
            parent = data[start];
            document.getElementById('commentList').innerHTML += render_group_comment(parent);
        } else {
            // start = stop;
            stop += 2;
            break;
        }
    }
    if (start == data.length) {
        $('#viewMoreComment').remove();
    }
}

function render_group_comment(parent) {
    var li = "<li class='comment root-comment'>";
    li += "<p id='comment_id'>" + parent.id + "</p><div class='vcard bio'><img src='/static/images/person_1.jpg' alt='Image placeholder'></div><div class='comment-body'><h3>" + replace_quotes(parent.author) + "</h3><div class='meta mb-3'>" + format_date(parent.created_at) + add_flag(parent.flag) + "</div><p>" + replace_quotes(parent.content) + "</p><a class='replycm'>Reply</a></div>"
    children = parent.children;
    if (children) {
        li += "<ul class='children'>";
        for (index in children) {
            child = children[index];
            li += "<li class='comment'><p id='comment_id'>" + child.id + "</p><div class='vcard bio'><img src='/static/images/person_1.jpg' alt='Image placeholder'></div><div class='comment-body'><h3>" + replace_quotes(child.author) + "</h3><div class='meta mb-3'>" + format_date(parent.created_at) + "</div><p>" + replace_quotes(child.reply) + "</p><p>" + replace_quotes(child.content) + "</p><a class='replycm'>Reply</a></div></li>";
        }
        li += "</ul>";
    }
    else {
        li += "<ul class='children'></ul>"
    }
    li += "</li>";
    return li;
}

function format_date(date) {
    return date.month + ". " + date.day + ", " + date.year + ", " + date.hour + ":" + date.minute + " " + date["AM-PM"]
    // return Nov. 17, 2020, 2:47 p.m.
}

function add_flag(is_flagged) {
    if (is_flagged) {
        return '<i style="position: relative; left:10px; color: red;" class="fas fa-flag"></i>'
    }
    else {
        return ""
    }
}

function replace_quotes(raw_string) {
    result = raw_string.replaceAll("'", '"');
    return result;
}

function standardize_request(raw_string) {
    return raw_string.replaceAll('"', "'").replaceAll("\\", "\\\\")
}



$(document).ready(function () {
    var post_id = document.getElementById("post_id").innerText;
    preload_comments(post_id);
})

window.onload = function () {
    var ps = document.getElementsByClassName("content");
    for (p of ps) { p.innerHTML = p.textContent }
}