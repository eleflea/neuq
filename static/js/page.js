$(document).ready(function () {
    (function () {
        String.prototype.replaceAll = function (exp, newStr) {
            return this.replace(new RegExp(exp, "gm"), newStr);
        };

        /**
         * 原型：字符串格式化
         * @param args 格式化参数值
         */
        String.prototype.format = function (args) {
            var result = this;
            if (arguments.length < 1) {
                return result;
            }

            var data = arguments;
            if (arguments.length == 1 && typeof (args) == "object") {
                data = args;
            }
            for (var key in data) {
                var value = data[key];
                if (undefined != value) {
                    result = result.replaceAll("\\{" + key + "\\}", value);
                }
            }
            return result;
        }

        if (!Array.prototype.shuffle) {
            Array.prototype.shuffle = function () {
                for (var j, x, i = this.length; i; j = parseInt(Math.random() * i), x = this[--i], this[i] = this[j], this[j] = x);
                return this;
            };
        }

        var is_ready = true;
        var head = 'data:image/png;base64,';
        var cmd = "if(this.className=='ublur'){this.className='blur';}else{this.className='ublur';}";
        var fmt = '<tr><td colspan="2" style="background-color: #eee;"><span class="label label-primary label-cus">{chapter}</span><span class="label label-primary label-cus">{diff}</span></td></tr><tr><td colspan="2"><img src="{img0}"></td></tr><tr><td onclick="{cmd1}"><img src="{img1}"></td><td onclick="{cmd2}"><img src="{img2}"></td></tr><tr><td onclick="{cmd3}"><img src="{img3}"></td><td onclick="{cmd4}"><img src="{img4}"></td></tr><tr><td colspan="2" class="blur" onclick="{cmd}"><img src="{img5}"></td></tr>';

        function ajax_load(page) {
            $.get("/question",
                { db: $("input[name='db']").val(), id: $("input[name='num']").val(), page: page },
                function (data, status) {
                    if (data.q.length < 5) {
                        is_ready = false;
                    }
                    data.q.forEach(function (element) {
                        o_array = [[1, 'togreen(this)'], [2, 'tored(this)'], [3, 'tored(this)'], [4, 'tored(this)']].shuffle();
                        $('tbody').append(fmt.format({
                            chapter: element.chapter,
                            diff: element.diff,
                            img0: head + element.imgs[0],
                            img1: head + element.imgs[o_array[0][0]],
                            img2: head + element.imgs[o_array[1][0]],
                            img3: head + element.imgs[o_array[2][0]],
                            img4: head + element.imgs[o_array[3][0]],
                            img5: head + element.imgs[5],
                            cmd: cmd,
                            cmd1: o_array[0][1],
                            cmd2: o_array[1][1],
                            cmd3: o_array[2][1],
                            cmd4: o_array[3][1]
                        }));
                    }, this);
                }
            );
        }

        $(window).scroll(function () {
            var bot = 50;
            if ((bot + $(window).scrollTop()) >= ($(document).height() - $(window).height()) && is_ready) {
                now_page = Number($("input[name='page']").val()) + 1;
                ajax_load(now_page);
                $("input[name='page']").val(now_page);
            }
        });
        ajax_load(1);
    })();
});

function togreen(th) {
    $(th).css("backgroundColor", "green");
    $(th).animate({
        backgroundColor: 'white'
    }, 600);
}

function tored(th) {
    $(th).css("backgroundColor", "red");
    $(th).animate({
        backgroundColor: 'white'
    }, 600);
}