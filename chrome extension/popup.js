function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min)) + min;
}

var raw_page = "";

chrome.extension.onRequest.addListener(function(request, sender, sendResponse) {
    raw_page = request.content;
});


document.addEventListener('DOMContentLoaded', function() {
    var clearMarkupList = document.getElementById('clearMarkupList');
    clearMarkupList.addEventListener('click', function() {

    d = document;
    var f = d.createElement('form');
    f.action = 'http://127.0.0.1:9876';
    f.method = 'post';
    var i = d.createElement('input');
    i.type = 'hidden';
    i.name = 'action';
    i.value = 'reset';
    f.appendChild(i);
    d.body.appendChild(f);
    f.submit();

    });
}, false);

document.addEventListener('DOMContentLoaded', function() {
    var actionLearn = document.getElementById('actionLearn');
    actionLearn.addEventListener('click', function() {

    d = document;
    var f = d.createElement('form');
    f.action = 'http://127.0.0.1:9876';
    f.method = 'post';
    var i = d.createElement('input');
    i.type = 'hidden';
    i.name = 'action';
    i.value = 'learn';
    f.appendChild(i);
    d.body.appendChild(f);
    f.submit();

    });
}, false);

document.addEventListener('DOMContentLoaded', function() {
    var actionParse = document.getElementById('actionParse');
    actionParse.addEventListener('click', function() {

    d = document;
    var f = d.createElement('form');
    f.action = 'http://127.0.0.1:9876';
    f.method = 'post';
    var i = d.createElement('input');
    i.id = "action";
    i.type = 'hidden';
    i.name = 'action';
    i.value = 'parse';
    f.appendChild(i);
    var j = d.createElement('input');
    j.type = 'hidden';
    j.name = 'raw_page';
    j.value = raw_page;
    f.appendChild(j);
    var k = d.createElement('iframe');
    k.id = 'response';
    k.name = 'response';
    f.target = '_blank';
    k.appendChild(f);
    k.onload = function(){
        if (document.getElementById("response"))
            alert(document.getElementById("response").innerHTML);
    };
    d.body.appendChild(k);
    f.submit();

    /*
        var fd = new FormData();
        fd.append("action", "parse");
        fd.append("raw_page", raw_page);

        var request = new XMLHttpRequest();
        request.open("POST", "http://127.0.0.1:9876");
        request.send(fd);
        if (request.status != 200) {
            alert("Error = " + request.status + ", " + request.statusText);
        } else {
            document.getElementById("markup").innerHTML = request.responseText;
        }
        */
    });
}, false);

document.addEventListener('DOMContentLoaded', function() {
    var sendMarkup = document.getElementById('sendMarkup');
    sendMarkup.addEventListener('click', function() {
        chrome.storage.sync.get("markup", function (obj) {
            if (obj.markup != null)
            {
                var fd = new FormData();
                fd.append("action", "add");
                var markup = {
                    components: obj.markup,
                    "py/object": "markups.search_markup.SearchMarkup",
                    "file": "0.html",
                };
                fd.append("markup", JSON.stringify(markup));
                fd.append("raw_page", raw_page);

                var request = new XMLHttpRequest();
                request.open("POST", "http://127.0.0.1:9876");
                request.send(fd);

            }
        });
    });
}, false);

document.addEventListener('DOMContentLoaded', function() {
    chrome.tabs.getSelected(null, function(tab) {
        chrome.tabs.executeScript(tab.id, {
            code: "chrome.extension.sendRequest({content: document.documentElement.outerHTML}, function(response) { console.log('success'); });"
        }, function() { });
    });

    var clearMarkup = document.getElementById('clearMarkup');
    clearMarkup.addEventListener('click', function() {
        chrome.storage.sync.set({'markup': null});
    });
}, false);

function getStringElement(title, value, key, index)
{
        var suf = getRandomInt(0, 999999);
        d = document;
        var div = d.createElement('div');
        var salign = d.createElement('span'); salign.innerHTML = title + ': ';
        div.appendChild(salign);
        var ialign = d.createElement('input'); ialign.value = value; ialign.id='align_' + suf;
        div.appendChild(ialign);
        var balign = d.createElement('button'); balign.innerHTML = 'Save'; balign.id = 'balign_' + suf;
        balign.addEventListener('click', function() {
            chrome.storage.sync.get("markup", function (obj) {
                obj.markup[index][key] = document.getElementById('align_' + suf).value;
                chrome.storage.sync.set({'markup': obj.markup});
            });
        });
        div.appendChild(balign);
        return div;
}

function getTreePathElement(title, value, key, index)
{
        var suf = getRandomInt(0, 999999);
        d = document;
        var div = d.createElement('div');
        var spage = d.createElement('span'); spage.innerHTML = title + ': ';
        div.appendChild(spage);
        var ipage = d.createElement('input'); ipage.value = value.xpath; ipage.id='page_xpath_' + suf;
        div.appendChild(ipage);
        var iattr = d.createElement('input'); iattr.value = value.attr; iattr.id='page_attr_' + suf; iattr.size = '5';
        div.appendChild(iattr);
        var bpage = d.createElement('button'); bpage.innerHTML = 'Save'; bpage.id = 'bpage_' + suf;
        bpage.addEventListener('click', function() {
            chrome.storage.sync.get("markup", function (obj) {
                obj.markup[index][key].xpath = document.getElementById('page_xpath_' + suf).value;
                obj.markup[index][key].attr = document.getElementById('page_attr_' + suf).value;
                chrome.storage.sync.set({'markup': obj.markup});
            });
        });
        div.appendChild(bpage);
        return div;
}

function getSearchResult(element, index)
{
        d = document;
        var div = d.createElement('div');
        var stype = d.createElement('span'); stype.innerHTML = '<br>SEARCH RESULT';
        div.appendChild(stype);
        div.appendChild(getStringElement('alignment', element.alignment, 'alignment', index));
        div.appendChild(getTreePathElement('page url', element.page_url, 'page_url', index));
        div.appendChild(getTreePathElement('title', element.title, 'title', index));
        div.appendChild(getTreePathElement('snippet', element.snippet, 'snippet', index));
        div.appendChild(getTreePathElement('view url', element.view_url, 'view_url', index));
        return div;
}

document.addEventListener('DOMContentLoaded', function() {
    var addSearchResult = document.getElementById('addSearchResult');
    addSearchResult.addEventListener('click', function() {

        chrome.storage.sync.get("markup", function (obj) {

            var element = {
                type: 'SEARCH_RESULT',
                alignment: 'LEFT',
                page_url: {xpath: '', attr: '', "py/object": "trees.html_path.HTMLPath"},
                title: {xpath: '', attr: '', "py/object": "trees.html_path.HTMLPath"},
                snippet: {xpath: '', attr: '', "py/object": "trees.html_path.HTMLPath"},
                view_url: {xpath: '', attr: '', "py/object": "trees.html_path.HTMLPath"},
                "py/object": "markups.search_markup.SearchMarkupSearchResult"
            };
            obj.markup[obj.markup.length] = element;
            chrome.storage.sync.set({'markup': obj.markup});

            d = document;
            var markup = d.getElementById('markup');
            var div = getSearchResult(element, obj.markup.length - 1);
            markup.appendChild(div);
        });
    });
}, false);


function getElem(element, index)
{
    if (element.type = "SEARCH_RESULT")
    {
        return getSearchResult(element, index);
    }
}

function currentList()
{
    chrome.storage.sync.get("markup", function (obj) {
        if (obj.markup != null)
        {
            markup = document.getElementById('markup');
            for (var i = 0; i < obj.markup.length; ++i)
            {
                var elem = getElem(obj.markup[i], i);
                markup.appendChild(elem);
            }
        }
        else
        {
            var markup = new Array(0);
            chrome.storage.sync.set({'markup': markup});
        }
    });
}

window.onload = currentList;