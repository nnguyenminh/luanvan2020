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
            var comment = "<li class='comment'><p id='comment_id' hidden>" + dataserver.id + "</p><div class='vcard bio'><img src='/static/images/person_1.jpg' alt='Image placeholder'></div><div class='comment-body'><h3>" + dataserver.author + "</h3><div class='meta mb-3'>" + dataserver.created_at + "</div><p>" + dataserver.content + "</p><p><button class='reply'>Reply</button></p></div></li>";
            x = comment + x;
            document.getElementById("commentList").innerHTML = x;
            $('#leaveCommentForm #message').val('');
        }
    });


    e.preventDefault();
});

// $("#replyCommentForm").on("submit", function (e) {
//     console.log("yes")
//     var post_id = document.getElementById("post_id").innerText
//     var author = $(this).find("#name").val();
//     var content = $(this).find("#message").val();
//     console.log(author);
//     console.log(content);
//     e.preventDefault();
// });
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
    //         var x = document.getElementById('commentList').innerHTML;
    //         var comment = "<li class='comment'><p id='comment_group_id' hidden>" + dataserver.id + "</p><div class='vcard bio'><img src='/static/images/person_1.jpg' alt='Image placeholder'></div><div class='comment-body'><h3>" + dataserver.author + "</h3><div class='meta mb-3'>" + dataserver.created_at + "</div><p>" + dataserver.content + "</p><p><a href='#' class='reply'>Reply</a></p></div></li>";
    //         x = comment + x;
    //         document.getElementById("commentList").innerHTML = x;
    //         $('#leaveCommentForm #message').val('');
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


$(document).on("click", ".reply", function (e) {

    $("#replyComment").remove();

    $(this).parent().parent().append(
        '<div class="comment-form-wrap pt-5" id="replyComment">' +
        '<form id="replyCommentForm" class="p-5 bg-light">' +
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

$(document).on('click', '#replyCommentForm button', function () {
    $("#replyCommentForm").remove();

})



var data;

const preload_comments = (id) => {
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
            //     document.getElementById('commentList').innerHTML = li;
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

// var commentCha = "<pid='comment_group_id'>comment.id</p><divclass='vcardbio'><imgsrc='{%static 'images/person_1.jpg' %}'alt='Imageplaceholder'></div><divclass='comment-body'><h3>comment.author</h3><divclass='metamb-3'>comment.created_at</div><p>comment.content</p><p><ahref='#'class='reply'>Reply</a></p></div>"


// var commentCon = "<liclass='comment'><divclass='vcardbio'><imgsrc='{%static 'images/person_1.jpg' %}'alt='Imageplaceholder'></div><divclass='comment-body'><h3>reply.author</h3><divclass='metamb-3'>reply.created_at</div><p>reply.reply</p><p>reply.content</p><p><ahref='#'class='reply'>Reply</a></p></div></li>"

function render_group_comment(parent) {
    children = parent.children;
    var li = "<li class='comment'>";
    li += "<p id='comment_id'>" + parent.id + "</p><div class='vcard bio'><img src='/static/images/person_1.jpg' alt='Image placeholder'></div><div class='comment-body'><h3>" + replace_quotes(parent.author) + "</h3><div class='meta mb-3'>" + parent.created_at + add_flag(parent.flag) + "</div><p>" + replace_quotes(parent.content) + "</p><p><button class='reply'>Reply</button></p></div>"
    li += "<ul class='children'>";
    for (index in children) {
        child = children[index];
        li += "<li class='comment'><p id='comment_id'>" + child.id + "</p><div class='vcard bio'><img src='/static/images/person_1.jpg' alt='Image placeholder'></div><div class='comment-body'><h3>" + replace_quotes(child.author) + "</h3><div class='meta mb-3'>" + child.created_at + "</div><p>" + replace_quotes(child.reply) + "</p><p>" + replace_quotes(child.content) + "</p><p><button class='reply'>Reply</button></p></div></li>";
    }
    li += "</ul></li>";
    return li
}

function add_flag(is_flagged) {
    if (is_flagged){
        return '<i style="position: relative; left:10px; color: red;" class="fas fa-flag"></i>'
    }    
}

function replace_quotes(raw_string) {
    result = raw_string.replaceAll("'",'"');
    return result;    
}

function standardize_request(raw_string) {
    return raw_string.replaceAll('"',"'").replaceAll("\\","\\\\")
}



$(document).ready(function () {
    var post_id = document.getElementById("post_id").innerText;
    preload_comments(post_id);
})

window.onload = function(){
    var ps = document.getElementsByClassName("content");
    for(p of ps) { p.innerHTML = p.textContent }
}