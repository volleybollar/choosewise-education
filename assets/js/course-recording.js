// course-recording.js
// In-browser 30-sec audio recording for modul 6 inspelningsövning.
// All processing happens locally — no uploads.
//
// Markup expected:
//   <div data-recorder>
//     <button data-start>Spela in 30 sek</button>
//     <button data-stop disabled>Stoppa</button>
//     <audio data-playback controls></audio>
//     <p data-status></p>
//   </div>
//
// Fallback: if no mic permission, show file upload <input type="file" accept="audio/*">.

(function (global) {
  function init() {
    const containers = document.querySelectorAll('[data-recorder]');
    containers.forEach(setup);
  }

  function setup(container) {
    const startBtn = container.querySelector('[data-start]');
    const stopBtn = container.querySelector('[data-stop]');
    const playback = container.querySelector('[data-playback]');
    const status = container.querySelector('[data-status]');

    let mediaRecorder = null;
    let chunks = [];
    let timeoutId = null;

    function setStatus(msg) { if (status) status.textContent = msg; }

    if (!navigator.mediaDevices?.getUserMedia) {
      setStatus('Din webbläsare stödjer inte inspelning. Ladda upp en ljudfil istället nedan.');
      addFallbackUpload(container, playback);
      return;
    }

    startBtn.addEventListener('click', async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        chunks = [];
        mediaRecorder.ondataavailable = (e) => { if (e.data.size) chunks.push(e.data); };
        mediaRecorder.onstop = () => {
          const blob = new Blob(chunks, { type: 'audio/webm' });
          playback.src = URL.createObjectURL(blob);
          stream.getTracks().forEach(t => t.stop());
          setStatus('Klar. Spela upp och lyssna efter utfyllnadsljud, pauser och tempo.');
        };
        mediaRecorder.start();
        startBtn.disabled = true;
        stopBtn.disabled = false;
        setStatus('Spelar in… 30 sek max.');

        timeoutId = setTimeout(() => {
          if (mediaRecorder?.state === 'recording') stopBtn.click();
        }, 30000);
      } catch (err) {
        setStatus('Kunde inte starta inspelning. Du kan ladda upp en ljudfil istället.');
        addFallbackUpload(container, playback);
      }
    });

    stopBtn.addEventListener('click', () => {
      if (mediaRecorder?.state === 'recording') mediaRecorder.stop();
      if (timeoutId) clearTimeout(timeoutId);
      startBtn.disabled = false;
      stopBtn.disabled = true;
    });
  }

  function addFallbackUpload(container, playback) {
    if (container.querySelector('input[type=file]')) return;
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'audio/*';
    input.style.marginTop = '1rem';
    input.addEventListener('change', () => {
      if (input.files[0]) {
        playback.src = URL.createObjectURL(input.files[0]);
      }
    });
    container.appendChild(input);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
  global.CourseRecording = { init };
})(window);
