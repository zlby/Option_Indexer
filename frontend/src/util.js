function hasClass(elem, cls) {
  cls = cls || '';
  if (cls.replace(/\s/g, '').length == 0) return false; //当cls没有参数时，返回false
  return new RegExp(' ' + cls + ' ').test(' ' + elem.className + ' ');
}
 
function addClass(ele, cls) {
  if (!hasClass(ele, cls)) {
    ele.className = ele.className == '' ? cls : ele.className + ' ' + cls;
  }
}
 
function removeClass(elem, cls) {
  if (hasClass(elem, cls)) {
    var newClass = ' ' + elem.className.replace(/[\t\r\n]/g, '') + ' ';
    while (newClass.indexOf(' ' + cls + ' ') >= 0) {
      newClass = newClass.replace(' ' + cls + ' ', ' ');
    }
    elem.className = newClass.replace(/^\s+|\s+$/g, '');
  }
}

function toggleBtn(btn) {
  if (hasClass(btn, 'el-button--primary')) {
    removeClass(btn, 'el-button--primary');
    addClass(btn, 'el-button--danger');
    removeClass(btn.children[0].children[0], 'el-icon-plus');
    addClass(btn.children[0].children[0], 'el-icon-minus');
  } else {
    removeClass(btn, 'el-button--danger');
    addClass(btn, 'el-button--primary');
    removeClass(btn.children[0].children[0], 'el-icon-minus');
    addClass(btn.children[0].children[0], 'el-icon-plus');
  } 
}

function setCookie(name, value, days) {
    var d = new Date;
    d.setTime(d.getTime() + 24*60*60*1000*days);
    window.document.cookie = name + "=" + value + ";path=/;expires=" + d.toGMTString();
}

function getCookie(name) {
    var v = window.document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return v ? v[2] : null;
}

function deleteCookie(name) {
    this.set(name, '', -1);
}

export {hasClass, addClass, removeClass, toggleBtn, getCookie};