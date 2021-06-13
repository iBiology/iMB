function playAudio(e, link) {
let audio = document.createElement("audio");
let src = document.createElement("source");
src.src = link.href;
audio.appendChild(src);
audio.play();
e.preventDefault();
}

document.getElementById('searchInput').addEventListener('keypress', function(event) {
    if (event.keyCode === 13) {
        event.preventDefault();
    }
});

