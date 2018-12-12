function result = checkBrowser(){

  var result = 'N/A';

  var agent = window.navigator.userAgent.toLowerCase();
  var version = window.navigator.appVersion.toLowerCase();

  if(agent.indexOf("msie") > -1){
    if (version.indexOf("msie 6.") > -1){
      result = 'IE6';
    }else if (version.indexOf("msie 7.") > -1){
      result = 'IE7';
    }else if (version.indexOf("msie 8.") > -1){
      result = 'IE8';
    }else if (version.indexOf("msie 9.") > -1){
      result = 'IE9';
    }else if (version.indexOf("msie 10.") > -1){
      result = 'IE10';
    }else{
      result = 'IE(N/A)';
    }
  }else if(agent.indexOf("trident/7") > -1){
    result = 'IE11';
  }else if(agent.indexOf("edge") > -1){
    result = 'Edge';
  }else if (agent.indexOf("chrome") > -1){
    result = 'Chrome';
  }else if (agent.indexOf("safari") > -1){
    result = 'Safari';
  }else if (agent.indexOf("opera") > -1){
    result = 'Opera';
  }else if (agent.indexOf("firefox") > -1){
    result = 'Firefox';
  }
}

function os = checkOS(){
  var os, ua = navigator.userAgent;

  if (ua.match(/Win(dows )?NT 10\.0/)) {
  	os = "Windows 10";				// Windows 10 の処理
  }
  else if (ua.match(/Win(dows )?NT 6\.3/)) {
  	os = "Windows 8.1";				// Windows 8.1 の処理
  }
  else if (ua.match(/Win(dows )?NT 6\.2/)) {
  	os = "Windows 8";				// Windows 8 の処理
  }
  else if (ua.match(/Win(dows )?NT 6\.1/)) {
  	os = "Windows 7";				// Windows 7 の処理
  }
  else if (ua.match(/Win(dows )?NT 6\.0/)) {
  	os = "Windows Vista";				// Windows Vista の処理
  }
  else if (ua.match(/Win(dows )?NT 5\.2/)) {
  	os = "Windows Server 2003";			// Windows Server 2003 の処理
  }
  else if (ua.match(/Win(dows )?(NT 5\.1|XP)/)) {
  	os = "Windows XP";				// Windows XP の処理
  }
  else if (ua.match(/Win(dows)? (9x 4\.90|ME)/)) {
  	os = "Windows ME";				// Windows ME の処理
  }
  else if (ua.match(/Win(dows )?(NT 5\.0|2000)/)) {
  	os = "Windows 2000";				// Windows 2000 の処理
  }
  else if (ua.match(/Win(dows )?98/)) {
  	os = "Windows 98";				// Windows 98 の処理
  }
  else if (ua.match(/Win(dows )?NT( 4\.0)?/)) {
  	os = "Windows NT";				// Windows NT の処理
  }
  else if (ua.match(/Win(dows )?95/)) {
  	os = "Windows 95";				// Windows 95 の処理
  }
  else if (ua.match(/Windows Phone/)) {
  	os = "Windows Phone";				// Windows Phone (Windows 10 Mobile) の処理

  	/*
  	if (ua.match(/Windows Phone( OS)? ([\.\d]+)/)) {
  		os = "Windows Phone "  + RegExp.$2;
  	}
  	else {
  		os = "Windows Phone";
  	}
  	*/
  }
  else if (ua.match(/iPhone|iPad/)) {
  	os = "iOS";					// iOS (iPhone, iPod touch, iPad) の処理

  	/*
  	if (ua.match(/(iPhone|CPU) OS ([\d_]+)/)) {
  		os = "iOS " + RegExp.$2;
  		os = os.replace(/_/g, ".");
  	}
  	else {
  		os = "iOS";
  	}
  	*/
  }
  else if (ua.match(/Mac|PPC/)) {
  	os = "Mac OS";					// Macintosh の処理

  	/*
  	if (ua.match(/OS X|MSIE 5\.2/)) {
  		if (ua.match(/Mac OS X ([\.\d_]+)/)) {
  			os = "macOS " + RegExp.$1;
  			os = os.replace(/_/g, ".");
  		}
  		else {
  			os = "macOS";
  		}
  	}
  	else {
  		os = "Classic Mac OS";
  	}
  	*/
  }
  else if (ua.match(/Android ([\.\d]+)/)) {
  	os = "Android " + RegExp.$1;			// Android の処理
  }
  else if (ua.match(/Linux/)) {
  	os = "Linux";					// Linux の処理
  }
  else if (ua.match(/^.*\s([A-Za-z]+BSD)/)) {
  	os = RegExp.$1;					// BSD 系の処理
  }
  else if (ua.match(/SunOS/)) {
  	os = "Solaris";					// Solaris の処理
  }
  else {
  	os = "N/A";					// 上記以外 OS の処理
  }
}
