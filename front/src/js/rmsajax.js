function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var rmsajax = {
    'get': function (args) {
        args['method'] = 'get';
        this.ajax(args);
    },
    'delete': function (args) {
        args['method'] = 'delete';
        this._ajaxSetup();
        this.ajax(args);
    },
    'post': function (args) {
        args['method'] = 'post';
        this._ajaxSetup();
        this.ajax(args);
    },
    'put': function (args) {
        args['method'] = 'put';
        this._ajaxSetup();
        this.ajax(args);
    },
    'ajax': function (args) {
        var success = args['success'];
        args['success'] = function (result) {
            if (result['code'] === 200) {
                if (success) {
                    success(result);
                }
            } else {
                var messageObject = result['message'];
                if (messageObject) {
                    if (typeof messageObject === 'string' || messageObject.constructor === String) {
                        layer.msg(messageObject, {icon: 2, time: 2000});
                    } else {
                        // {"password":['密码最大长度不能超过20为！','xxx'],"telephone":['xx','x']}
                        var message="";
                        for (var key in messageObject) {
                            message = messageObject[key]+"<br>"+message
                        }
                        layer.msg(message, {icon: 2, time: 2000});

                    }
                }
                if (success) {
                    success(result);
                }
            }
        };
        args['fail'] = function (error) {
            console.log(error);
            // window.messageBox.showError('服务器内部错误！');
            layer.msg('服务器内部错误！', {icon: 2, time: 2000});
        };
        $.ajax(args);
    },
    '_ajaxSetup': function () {
        $.ajaxSetup({
            cache: false,
            beforeSend: function (xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            }
        });
    }
};
