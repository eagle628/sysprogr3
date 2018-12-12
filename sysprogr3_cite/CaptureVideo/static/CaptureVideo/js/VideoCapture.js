var video = document.querySelector("video");
var constraints = {
  audio: false,
  video: {
    // スマホのバックカメラを使用
    facingMode: { exact : "environment"},
    frameRate: { ideal: 10, max: 15 },
    width: 1920,
    height: 1080
  }
};

// カメラから映像を取得
var item = navigator.mediaDevices.getUserMedia(constraints)

// Role of button
var button = document.getElementById('button');

function adjustVideo() {
  // 映像が画面幅いっぱいに表示されるように調整
  var ratio = window.innerWidth / video.videoWidth;

  video.width = window.innerWidth;
  video.height = video.videoHeight * ratio;
  canvas.width = video.width;
  canvas.height = video.height;
}

function onDown(e) {
  console.log("down");
}

function onUp(e) {
  console.log("up");
}

function onClick(e) {
  console.log("click");
}

function onOver(e) {
  console.log("mouseover");
}

function onOut() {
  console.log("mouseout");
}

function CaptureShot(){
  // video stop
  //video.pause();
  var canvas = document.getElementById('canvas');
  var ctx = canvas.getContext('2d');

  //videoのstreamをcanvasに書き出す方法
  //videoの縦幅横幅を取得
  var w = video.offsetWidth;
  var h = video.offsetHeight;
  canvas.setAttribute("width", w);
  canvas.setAttribute("height", h);
  ctx.drawImage(video, 0, 0, w, h);

  //canvasを更にimgに書き出す方法
  var img = document.getElementById('img');
  //console.log(img.src)
  img.src = canvas.toDataURL('image/png');

}


item.then((stream) => {
    video.srcObject = stream;
    // 動画のメタ情報のロードが完了したら実行
    video.onloadedmetadata = function(mediaStream) {
      console.log('取得したMediaStream->', mediaStream);
      videoStreamInUse = mediaStream;
      //ロード完了後にカメラの設定
      button.addEventListener('click', CaptureShot);
      //video.addEventListener('click', CaptureShot)
      //adjustVideo();
    };
  })
  .catch((err) => {
    window.alert(err.name + ': ' + err.message);
});


/*
canvas.addEventListener('mousedown', onDown, false);
canvas.addEventListener('mouseup', onUp, false);
canvas.addEventListener('click', onClick, false);
canvas.addEventListener('mouseover', onOver, false);
canvas.addEventListener('mouseout', onOut, false);
*/
