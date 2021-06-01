// refer to https://www.otwo.jp/blog/canvas-drawing/

var canvases = [];
var contexts = [];
const canvasWidth = 100;
const canvasHeight = 100;
var canvasColor = "0, 0, 0, 1"
var canvasBold = 5;

var clickFlag = 0;  //1:クリック開始, 2:クリック中

for (let i = 0; i < 7; i++){
    var canvas_id = 'canvas' + i;
    var canvas = document.getElementById(canvas_id);
    canvases.push(canvas);
    var context = canvas.getContext('2d');
    contexts.push(context);
    setBackgroundColor(context);
}

$('#canvas0').mousedown(function(){
    clickFlag = 1;
}).mouseup(function(){
    clickFlag = 0;
}).mousemove(function(e){
    if(!clickFlag) return false;
    draw(contexts[0], e.offsetX, e.offsetY);
});

$('#clear0').click(function(){
    contexts[0].clearRect(0, 0, canvasWidth, canvasHeight);
    setBackgroundColor(contexts[0]);
})

$('#canvas1').mousedown(function(){
    clickFlag = 1;
}).mouseup(function(){
    clickFlag = 0;
}).mousemove(function(e){
    if(!clickFlag) return false;
    draw(contexts[1], e.offsetX, e.offsetY);
});

$('#clear1').click(function(){
    contexts[1].clearRect(0, 0, canvasWidth, canvasHeight);
    setBackgroundColor(contexts[1]);
})

$('#canvas2').mousedown(function(){
    clickFlag = 1;
}).mouseup(function(){
    clickFlag = 0;
}).mousemove(function(e){
    if(!clickFlag) return false;
    draw(contexts[2], e.offsetX, e.offsetY);
});

$('#clear2').click(function(){
    contexts[2].clearRect(0, 0, canvasWidth, canvasHeight);
    setBackgroundColor(contexts[2]);
})

$('#canvas3').mousedown(function(){
    clickFlag = 1;
}).mouseup(function(){
    clickFlag = 0;
}).mousemove(function(e){
    if(!clickFlag) return false;
    draw(contexts[3], e.offsetX, e.offsetY);
});

$('#clear3').click(function(){
    contexts[3].clearRect(0, 0, canvasWidth, canvasHeight);
    setBackgroundColor(contexts[3]);
})

$('#canvas4').mousedown(function(){
    clickFlag = 1;
}).mouseup(function(){
    clickFlag = 0;
}).mousemove(function(e){
    if(!clickFlag) return false;
    draw(contexts[4], e.offsetX, e.offsetY);
});

$('#clear4').click(function(){
    contexts[4].clearRect(0, 0, canvasWidth, canvasHeight);
    setBackgroundColor(contexts[4]);
})

$('#canvas5').mousedown(function(){
    clickFlag = 1;
}).mouseup(function(){
    clickFlag = 0;
}).mousemove(function(e){
    if(!clickFlag) return false;
    draw(contexts[5], e.offsetX, e.offsetY);
});

$('#clear5').click(function(){
    contexts[5].clearRect(0, 0, canvasWidth, canvasHeight);
    setBackgroundColor(contexts[5]);
})

$('#canvas6').mousedown(function(){
    clickFlag = 1;
}).mouseup(function(){
    clickFlag = 0;
}).mousemove(function(e){
    if(!clickFlag) return false;
    draw(contexts[6], e.offsetX, e.offsetY);
});

$('#clear6').click(function(){
    contexts[6].clearRect(0, 0, canvasWidth, canvasHeight);
    setBackgroundColor(contexts[6]);
})

function draw(context, x, y) {
    context.lineWidth = canvasBold;
    context.strokeStyle = 'rgba(' + canvasColor + ')';
    if (clickFlag == "1") {
        clickFlag = "2";
        context.beginPath();
        context.lineCap = "round";
        context.moveTo(x, y);
    }
    else {
        context.lineTo(x, y);
    }
    context.stroke();
}

function setBackgroundColor(context) {
    context.fillStyle = "rgb(255,255,255)";
    context.fillRect(0, 0, canvasWidth, canvasHeight);
}

$(function(){
    $('button#search').bind('click', function(){
        let base64 = saveImage();
        $.getJSON('/_display', {
            num0: base64[0], 
            num1: base64[1], 
            num2: base64[2], 
            num3: base64[3], 
            num4: base64[4], 
            num5: base64[5], 
            num6: base64[6], 
        }, function(result){
            showResult(result);
        });
    });
});

function clearResult(){
    $("#zip_code").text("");
    $("#address").text("");
    $("#message").text("");
}

function showResult(result){
    clearResult();
    console.log(result);
    
    zip_code = "〒" + result.zip_code.slice(0, 3) + "-" + result.zip_code.slice(3, 7);
    $("#zip_code").text(zip_code);

    status = result.code;
    if (status != 200){
        var message = '住所が見つかりませんでした。';
        $("#message").text(message);
        return;
    }

    $("#address").text(result.data.fullAddress);
}

function saveImage(){ 
    var base64 = []
    for (let i = 0; i < 7; i++){
        url = canvases[i].toDataURL('image/jpeg');
        base64.push(url);
    }

    return base64;
}