// Setup Youtube Iframe API
var tag = document.createElement('script');
tag.id = 'youtube-iframe-api';
tag.src = 'https://www.youtube.com/iframe_api';
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// Configure player instance
var player;
function onYouTubeIframeAPIReady() {
    player = new YT.Player('video-player', {
        events: {
          'onReady': onPlayerReady,
          'onStateChange': onPlayerStateChange,
          'onError': onPlayerError
        }
    });
}
function onPlayerReady(event) {
}
function onPlayerStateChange(event) {
}
function onPlayerError(event) {
}