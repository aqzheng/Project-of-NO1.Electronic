/*
 * HjPager
 *
 * [注：父元素添加默认样式类：.pager]
 *
 * 配置项：
 * element: null,    // DOM-BOX
 * buttonCount: 10,  // 页面显示的页码按钮数量
 * currentPage: 1,   // 当前页
 * totalPage: 1,     // 总页数
 * globalJump: false // 是否开启输入跳转功能
 * firstBtn: false   // 是否加入`首页`按钮
 * lastBtn: false    // 是否加入`末页`按钮
 * pageQuery: '',    // '' - [默认值] 通过事件监听来隐式换页；'page' - 通过 url 中的 page 参数来切换页码和定位当前页
 * templates: {      // 自定义样式时使用
 *     number: '<span>%page%</span>',
 *     prev: '<button class=prev>上一页</button>',
 *     next: '<button class=next>下一页</button>',
 *     first: '<button class=first>首页</button>',
 *     last: '<button class=last>末页</button>'
 * },
 * pageChange: function (num) { // 默认翻页回调
 *     console.log(num)
 * }
 *
 * 调用：
 *
 * DOM: <div class="pager" id="pager"></div>
 *
 * var pagerBox = document.getElementById('pager');
 *
 * 1.在控制台输出页码
 * new window.HjPager({ // 注：不要重复新建实例！
 *     element: pagerBox,
 *     currentPage: 1,
 *     totalPage: 50,
 *     pageChange: function (num) {
 *         console.log(num)
 *     }
 * });
 *
 * 2.改变url，添加 search 参数 &page=1...
 * new HjPager({
 *     element: pagerBox,
 *     currentPage: parseInt(HjPager.get('page'), 10), // HjPager.get(name) 方法获取 url-search 中指定 name 的值
 *     totalPage: 50,
 *     pageQuery: 'page'
 * });
 *
 */
(function () {

    'use strict';

    var tool = {
        on: function (element, eventType, selector, fn) {
            element.addEventListener(eventType, function (e) {
                var el = e.target;

                if (!Element.prototype.matches) {
                    Element.prototype.matches =
                        Element.prototype.matchesSelector ||
                        Element.prototype.mozMatchesSelector ||
                        Element.prototype.msMatchesSelector ||
                        Element.prototype.oMatchesSelector ||
                        Element.prototype.webkitMatchesSelector ||
                        function (s) {
                            var matches = (this.document || this.ownerDocument).querySelectorAll(s),
                                i = matches.length;
                            while (--i >= 0 && matches.item(i) !== this) {
                            }
                            return i > -1
                        }
                }
                while (!el.matches(selector)) {
                    if (element === el) {
                        el = null;
                        break
                    }
                    el = el.parentNode
                }
                el && fn.call(el, e, el)
            });
            return element
        },
        create: function (html, children) {
            var template = document.createElement('template');
            if (!String.prototype.trim) {
                String.prototype.trim = function () {
                    return this.replace(/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g, '')
                }
            }
            template.innerHTML = html.trim();
            var node = template.content ? template.content.firstChild : template.childNodes[0];
            if (children) this.append(node, children);
            return node
        },
        append: function (parent, children) {
            if (children.length === undefined) children = [children];
            for (var i = 0; i < children.length; i++) {
                parent.appendChild(children[i])
            }
            return parent
        },
        paraType: function (para) {
            return Object.prototype.toString.call(para)
        }
    };

    var encode = encodeURIComponent,
        decode = decodeURIComponent;

    function HjPager(options) {

        var t = this;

        var _DEFAULT_ = {
            element: null,
            buttonCount: 5,
            currentPage: 1,
            totalPage: 1,
            pageQuery: '', // 'page'
            globalJump: false,
            firstBtn: false,
            lastBtn: false,
            templates: {
                number: '%page%', // '<span>%page%</span>'
                prev: '<button class=prev>上一页</button>',
                next: '<button class=next>下一页</button>',
                first: '<button class=first>首页</button>',
                last: '<button class=last>末页</button>'
            },
            pageChange: function (num) {
            }
        };

        if (!(t instanceof HjPager)) throw new TypeError('Cannot call a class as a function');

        t.options = t.extend(_DEFAULT_, options);
        t.domRefs = {};
        t.currentPage = parseInt(t.options.currentPage, 10) || 1;
        if (t.currentPage > t.options.totalPage) t.currentPage = t.options.totalPage;
        t.checkOptions().initHtml().bindEvents()
    }

    /**
     * 获取 url 携带的全部或指定参数
     * @param name
     * return obj
     */
    HjPager.get = function (name) {

        function getAll(searchStr) {
            var query = searchStr.replace(/^\?/, ''),
                queryObject = {},
                tmp = [];

            if (!query) return queryObject;

            query.split('&').filter(function (i) {
                return i
            }).forEach(function (str, index) {
                tmp = str.split('=');
                queryObject[tmp[0]] = decode(tmp[1])
            });

            return queryObject
        }

        if (!arguments.length) return getAll(location.search);

        return getAll(location.search)[name]
    };
    /**
     * 设置 url 中的参数和值 - set('a', 'b') || set({a: 'b', c: 'd'})
     * @param name
     * @param value
     */
    HjPager.set = function (name, value) {

        var ser = location.search;

        function set(search, name, value) {
            var regex = new RegExp('(' + encode(name) + ')=([^&]*)', '');
            if (regex.test(search)) {
                return search.replace(regex, function (match, c1, c2) {
                    return c1 + '=' + encode(value)
                })
            }
            return search.replace(/&?$/, '&' + encode(name) + '=' + encode(value))
        }

        if (arguments.length === 1 && tool.paraType(name) === '[object Object]') {
            for (var key in arguments[0]) {
                if (arguments[0].hasOwnProperty(key)) ser = set(ser, key, arguments[0][key])
            }
        } else {
            ser = set(ser, name, value)
        }
        location.search = ser
    };

    HjPager.prototype = {
        extend: function () {
            var len = arguments.length,
                i = 1,
                target = arguments[0] || {};

            if (Object.prototype.toString.call(target) !== '[object Object]') target = {};
            if (i === len) {
                target = this;
                i--
            }
            for (; i < len; i++) {
                if (arguments[i] != null) {
                    for (var key in arguments[i]) {
                        if (arguments[i][key] !== undefined && arguments[i].hasOwnProperty(key)) target[key] = arguments[i][key]
                    }
                }
            }
            return target
        },
        checkOptions: function () {
            if (!this.options.element) throw new Error('element is required');
            return this
        },
        bindEvents: function () {
            var t = this;

            tool.on(t.options.element, 'click', 'ol[data-role="pageNumbers"]>li', function (e, el) {
                e.stopPropagation();
                t.goToPage(parseInt(el.dataset ? el.dataset.page : el.textContent, 10))
            });

            t.options.firstBtn &&
            t.domRefs.first.addEventListener('click', function (e) {
                e.stopPropagation();
                t.goToPage(1)
            });

            t.options.lastBtn &&
            t.domRefs.last.addEventListener('click', function (e) {
                e.stopPropagation();
                t.goToPage(t.options.totalPage)
            });

            t.domRefs.prev.addEventListener('click', function (e) {
                e.stopPropagation();
                t.goToPage(t.currentPage - 1)
            });
            t.domRefs.next.addEventListener('click', function (e) {
                e.stopPropagation();
                t.goToPage(t.currentPage + 1)
            });
            t.options.element.addEventListener('pageChange', function (e) {
                t.options.pageChange(e);
            });

            t.options.globalJump &&
            t.domRefs.globalJump.addEventListener('click', function (e) {
                e.stopPropagation();
                var val = parseInt(t.domRefs.input.value, 10);
                t.domRefs.input.value = '';

                if (!val || val > t.options.totalPage || val === t.currentPage || val < 0) return;
                t.goToPage(val)
            })
        },
        goToPage: function (page) {
            var t = this;
            if (tool.paraType(page) !== '[object Number]') page = parseInt(page, 10);
            if (!page || page > t.options.totalPage || page === t.currentPage || page < 0) return;
            if (t.options.pageQuery === 'page') {
                HjPager.set(t.options.pageQuery, page)
            } else {
                // this.options.element.dispatchEvent(new CustomEvent('pageChange', {detail: {page: page}}));
                // this.options.element.addEventListener('pageChange', function (e) {
                //     _this.options.pageChange(e);
                // });
                t.options.pageChange(page)
            }
            t.currentPage = page;
            t.reRender()
        },
        reRender: function () {
            var t = this,
                newNumbers, oldNumbers;
            t._checkButtons();
            newNumbers = t._createNumbers();
            oldNumbers = t.domRefs.numbers;
            oldNumbers.parentNode.replaceChild(newNumbers, oldNumbers);
            t.domRefs.numbers = newNumbers
        },
        initHtml: function () {
            var t = this,
                pager = t.domRefs.pager = document.createElement('div');
            t.domRefs.first = t.options.firstBtn ? tool.create(t.options.templates.first) : null;
            t.domRefs.prev = tool.create(t.options.templates.prev);
            t.domRefs.next = tool.create(t.options.templates.next);
            t.domRefs.last = t.options.lastBtn ? tool.create(t.options.templates.last) : null;
            t._checkButtons();
            t.domRefs.numbers = t._createNumbers();

            t.options.firstBtn && pager.appendChild(t.domRefs.first);
            pager.appendChild(t.domRefs.prev);
            pager.appendChild(t.domRefs.numbers);
            pager.appendChild(t.domRefs.next);
            t.options.lastBtn && pager.appendChild(t.domRefs.last);

            if (t.options.globalJump && tool.paraType(t.options.globalJump) === '[object Boolean]') {
                var span = tool.create('<span class="jump-title">共' + t.options.totalPage + '页，跳转到：</span>');
                t.domRefs.input = tool.create('<input class="jump-input">');
                t.domRefs.globalJump = tool.create('<button class="jump-btn">确认</button>>');
                pager.appendChild(span);
                pager.appendChild(t.domRefs.input);
                pager.appendChild(t.domRefs.globalJump)
            } else {
                t.options.globalJump = false
            }

            t.options.element.innerHTML = '';
            t.options.element.appendChild(pager);
            t.options.element = pager;
            return t
        },
        _checkButtons: function () {
            var t = this,
                disabled = 'disabled';
            if (t.currentPage === 1) {
                t.options.firstBtn && t.domRefs.first.setAttribute(disabled, '');
                t.domRefs.prev.setAttribute(disabled, '')
            } else {
                t.options.firstBtn && t.domRefs.first.removeAttribute(disabled);
                t.domRefs.prev.removeAttribute(disabled)
            }
            if (t.currentPage === t.options.totalPage) {
                t.domRefs.next.setAttribute(disabled, '');
                t.options.lastBtn && t.domRefs.last.setAttribute(disabled, '')
            } else {
                t.domRefs.next.removeAttribute(disabled);
                t.options.lastBtn && t.domRefs.last.removeAttribute(disabled)
            }
        },
        _createNumbers: function () {
            var t = this,
                currentPage = t.currentPage,
                _options = t.options,
                buttonCount = _options.buttonCount,
                totalPage = _options.totalPage;

            var start1 = Math.max(currentPage - Math.round(buttonCount / 2) + 1, 1),
                end1 = Math.min(start1 + buttonCount - 1, totalPage),
                end2 = Math.min(currentPage + Math.round(buttonCount / 2) - 1, totalPage),
                start2 = Math.max(end2 - buttonCount + 1, 1),
                start = Math.min(start1, start2),
                end = Math.max(end1, end2);

            var ol = tool.create('<ol data-role="pageNumbers"></ol>');

            for (var i = start; i <= end; i++) {
                var li = tool.create('<li data-page="' + i + '"' + (i > 99999 ? ' title="' + i + '"' : '') + '>' + t.options.templates.number.replace('%page%', i) + '</li>');
                if (i === currentPage) li.classList ? li.classList.add('current') : li.className = 'current';
                ol.appendChild(li)
            }
            return ol
        }
    };

    window.HjPager = HjPager;

    return HjPager

})();