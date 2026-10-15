
/** @type{NodeListOf<HTMLVideoElement>} */
const videos_to_predownload = document.querySelectorAll("video[predownload]");

for (const video of videos_to_predownload) {
  if (!video.src) continue;
  console.log("Predownloading:", video.src);

  const { update: on_progress, done, error } = createSpinner(video);
  const old_src = video.src;
  video.src = "";
    downloadToBlob(old_src, on_progress).then(url => video.src = url).catch(e => {
        console.error(e);
        video.src = old_src;
    }).finally(done);
}

/**
 * Wraps `video` in a positioned container and injects a spinner + percent overlay.
 * Returns { update(pct), done(), error() }.
 */
function createSpinner(video) {
    // Wrap the video so the overlay can be absolutely positioned over it
  const wrapper = document.createElement("div");
    wrapper.style.position = "relative";
    wrapper.style.display = "inline-block";
    wrapper.style.display = "flex";
    wrapper.style.justifyContent = "center";
    video.parentNode.insertBefore(wrapper, video);
    wrapper.appendChild(video);

    const overlay = document.createElement("div");
    overlay.className = "predownload-overlay";
    overlay.innerHTML = `
    <div class="predownload-spinner"></div>
    <div class="predownload-pct">0%</div>
  `;
    wrapper.appendChild(overlay);

    const pctEl = overlay.querySelector(".predownload-pct");

    return {
        update(pct) {
            pctEl.textContent = pct + "%";
        },
        done() {
            overlay.remove();
        },
        error() {
            overlay.innerHTML = `<div class="predownload-pct">Failed to preload</div>`;
            setTimeout(() => overlay.remove(), 2000);
        }
    };
}



/**
Prefetch the video, return the fully fetched URL
 */
async function downloadToBlob(url, onProgress) {
  const response = await fetch(url);
  const content_length_header = response.headers.get('Content-Length');
  if (!content_length_header) return url;
  const content_length = parseInt(content_length_header);
  if (isNaN(content_length) || content_length <= 0) return url;
  const reader = response.body.getReader();
  
  let received = 0;
  const chunks = [];
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    chunks.push(value);
    received += value.length;
    const rounded_pct = Math.floor(100 * received / content_length);
    onProgress(rounded_pct);
  }

  const blob = new Blob(chunks);
  return URL.createObjectURL(blob);
}
