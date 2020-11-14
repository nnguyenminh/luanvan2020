$("#post_comment").on("submit", function (e) {
    var post_id = document.getElementById("post_id").innerText;
    var author = $(this).find("#name").val();
    var content = $(this).find("#message").val();
    var dataString = '{ "post_id":"' + post_id + '",' +
        '"author":"' + author + '",' +
        '"content":"' + content + '"' +
        '}';

    $.ajax({
        type: "POST",
        url: "/blog/post_comment",
        contentType: 'application/json',
        data: dataString,
        success: function (dataserver) {
            var x = document.getElementById('fatherfather').innerHTML;
            var comment = "<li class='comment'><p id='comment_id' hidden>" + dataserver.id + "</p><div class='vcard bio'><img src='/static/images/person_1.jpg' alt='Image placeholder'></div><div class='comment-body'><h3>" + dataserver.author + "</h3><div class='meta mb-3'>" + dataserver.created_at + "</div><p>" + dataserver.content + "</p><p><button class='reply'>Reply</button></p></div></li>";
            x = comment + x;
            document.getElementById("fatherfather").innerHTML = x;
            $('#post_comment #message').val('');
        }
    });


    e.preventDefault();
});

$("#popup_comment").on("submit", function (e) {
    console.log("yes")
    var post_id = document.getElementById("post_id").innerText
    var author = $(this).find("#name").val();
    var content = $(this).find("#message").val();
    console.log(author);
    console.log(content);
    e.preventDefault();
});
    // var dataString = '{ "post_id":"' + post_id + '",' +
    //     '"author":"' + author + '",' +
    //     '"content":"' + content + '"' +
    //     '}'
    // console.log(dataString)

    // $.ajax({
    //     type: "POST",
    //     url: "/blog/post_comment",
    //     contentType: 'application/json',
    //     data: dataString,
    //     success: function (dataserver) {
    //         var x = document.getElementById('fatherfather').innerHTML;
    //         var comment = "<li class='comment'><p id='comment_group_id' hidden>" + dataserver.id + "</p><div class='vcard bio'><img src='/static/images/person_1.jpg' alt='Image placeholder'></div><div class='comment-body'><h3>" + dataserver.author + "</h3><div class='meta mb-3'>" + dataserver.created_at + "</div><p>" + dataserver.content + "</p><p><a href='#' class='reply'>Reply</a></p></div></li>";
    //         x = comment + x;
    //         document.getElementById("fatherfather").innerHTML = x;
    //         $('#post_comment #message').val('');
    //     }
    // })




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

var reply_state = false;

$(document).on("click", ".reply", function (e) {

    $("#popup_comment").remove();

    $(this).parent().parent().append(
        '<div class="comment-form-wrap pt-5">' +
        '<form id="popup_comment" class="p-5 bg-light">' +
        '<div class="form-group">' +
        '<label for="name">Name *</label>' +
        '<input type="text" class="form-control" id="name" required>' +
        '</div>' +
        '<div class="form-group">' +
        '<label for="message">Message *</label>' +
        '<textarea name="" id="message" cols="30" rows="10" class="form-control" required></textarea>' +
        '</div>' +
        '<div class="form-group">' +
        '<input type="submit" value="Post Comment" class="btn py-3 px-4 btn-primary">' +
        '<button class="btn">Close</button>' +
        '</div>' +
        '</form>' +
        '</div>');

    e.preventDefault();
});

$(document).on('click', '#popup_comment button', function () {
    $("#popup_comment").remove();

})



var data;

const sayHello = (id) => {
    $.ajax("/blog/load_comments/post=" + id, {
        success: function (dataserver, status, xhr) {
            data = dataserver.reverse();
            // var len = length(data);
            // data.forEach((comment) => {
            //     var li = "<li class='comment'>";
            //     li += "<p id='comment_group_id'>" + comment.id + "</p><div class='vcard bio'><img src='/static/images/person_1.jpg' alt='Image placeholder'></div><div class='comment-body'><h3>" + comment.author + "</h3><div class='meta mb-3'>" + comment.created_at + "</div><p>" + comment.content + "</p><p><a href='#' class='reply'>Reply</a></p></div>"
            //     li += "<ul class='children'>";
            //     comment.children.forEach((reply) => {
            //         li += "<li class='comment'><div class='vcard bio'><img src='/static/images/person_1.jpg' alt='Image placeholder'></div><div class='comment-body'><h3>" + reply.author + "</h3><div class='meta mb-3'>" + reply.created_at + "</div><p>" + reply.reply + "</p><p>" + reply.content + "</p><p><a href='#' class='reply'>Reply</a></p></div></li>";
            //     })
            //     li += "</ul></li>";
            //     document.getElementById('fatherfather').innerHTML = li;
            // })
            loadComment();
        }
    })
}

var start = 0;
var stop = 1;

var loadComment = () => {
    // alert(data.length);
    // var max = 1;
    // var len = document.getElementById('fatherfather').childElementCount;
    for (start; start < data.length; start++) {
        if (start <= stop) {
            parent = data[start];
            children = parent.children;
            var li = "<li class='comment'>";
            li += "<p id='comment_id'>" + parent.id + "</p><div class='vcard bio'><img src='/static/images/person_1.jpg' alt='Image placeholder'></div><div class='comment-body'><h3>" + parent.author + "</h3><div class='meta mb-3'>" + parent.created_at + "</div><p>" + parent.content + "</p><p><button class='reply'>Reply</button></p></div>"
            li += "<ul class='children'>";
            for (index in children) {
                child = children[index];
                li += "<li class='comment'><p id='comment_id'>" + child.id + "</p><div class='vcard bio'><img src='/static/images/person_1.jpg' alt='Image placeholder'></div><div class='comment-body'><h3>" + child.author + "</h3><div class='meta mb-3'>" + child.created_at + "</div><p>" + child.reply + "</p><p>" + child.content + "</p><p><button class='reply'>Reply</button></p></div></li>";
            }
            li += "</ul></li>";
            document.getElementById('fatherfather').innerHTML += li;
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

// var commentCha = "<pid='comment_group_id'>comment.id</p><divclass='vcardbio'><imgsrc='{%static 'images/person_1.jpg' %}'alt='Imageplaceholder'></div><divclass='comment-body'><h3>comment.author</h3><divclass='metamb-3'>comment.created_at</div><p>comment.content</p><p><ahref='#'class='reply'>Reply</a></p></div>"


// var commentCon = "<liclass='comment'><divclass='vcardbio'><imgsrc='{%static 'images/person_1.jpg' %}'alt='Imageplaceholder'></div><divclass='comment-body'><h3>reply.author</h3><divclass='metamb-3'>reply.created_at</div><p>reply.reply</p><p>reply.content</p><p><ahref='#'class='reply'>Reply</a></p></div></li>"






$(document).ready(function () {
    var post_id = document.getElementById("post_id").innerText;
    sayHello(post_id);
})
