/**
 * Created by Carl on 2017/11/23.
 */
;
js_comm = {
    ajax_lock: false,
    obj_modal: null,

    ini: function() {
        // init alert modal
        if (!$('#Gantt-Alert-Modal').length > 0) {
            //$('body').append('<div id="Gantt-Alert-Modal" class="modal"></div>');
        }
        $('.checkAll').on('click', function(){
            $('input[name="'+$(this).data('target')+'"]').prop('checked', $(this).prop('checked'));
        });
        // init common modal
        js_comm.obj_modal = $('#commonModal');
        // datepicker
        $('.datepicker').datepicker({
            daysOfWeekHighlighted: "0,6",
            language: "zh-CN",
        });
    },
    alert: function(content, alert_cls, _callbk) {
        alert_cls = alert_cls || 'danger';
        var _content = '<div class=""></div>';
            _content+= '<div class="">' + content + '</div>';
            _content+= '<div class=""></div>';
        //$('#Gantt-Alert-Modal').html(_content).on('hidden.bs.modal', _callbk).modal('show');
        alert(content);
        _callbk();
    },
    alert_success: function(content, _callbk) {
        js_comm.alert(content, 'success', _callbk);
    },
    alert_error: function(content, _callbk) {
        js_comm.alert(content, 'danger', _callbk);
    },
    ajax: function(_url, _data, _ok, _fail) {
        if (js_comm.ajax_lock) {
            return false;
        }
        $.ajax({
            url: _url,
            type: 'POST',
            data: _data,
            dataType: 'JSON',
            timeOut: 15000,
            success: function(res) {
                if (res.status === 0) {
                    _ok(res);
                } else {
                    if (_fail) {
                        _fail(res);
                    } else {
                        js_comm.alert_error(res.content);
                    }
                }
            },
            error: function(xhr, status, err) {
                js_comm.alert_error('系统出错了：' + err);
            },
            complete: function() {
                js_comm.ajax_lock = false;
            }
        })
    },
    ajax_get: function(_url, _ok) {
        $.ajax({
            url: _url,
            type: 'GET',
            dataType: 'text',
            timeOut: 15000,
            success: function(res) {
                _ok(res);
            },
            error: function(xhr, status, err) {
                js_comm.alert_error('系统出错了：' + err);
            }
        })
    },
    ajax_form: function(_form, _ok, _fail) {
        js_comm.ajax($(_form).attr('action'), $(_form).serialize(), _ok, _fail);
    },
    load_modal: function(_url, _cb) {
        js_comm.ajax_get(_url, function(res){
            js_comm.obj_modal.html(res).modal('show');
            if (_cb) {
                _cb();
            }
        });
    },
    modal: function(content, _cb) {
        js_comm.obj_modal.html(content);
        js_comm.obj_modal.modal('show');
        if (_cb) {
            _cb();
        }
    }
};
$(function(){js_comm.ini();});