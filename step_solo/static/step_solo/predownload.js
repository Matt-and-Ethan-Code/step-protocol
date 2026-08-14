
/** @type{NodeListOf<HTMLVideoElement>} */
const videos_to_predownload = document.querySelectorAll("video[predownload]");

for (const video of videos_to_predownload) {
  if (!video.src) continue;
  console.log("Predownloading:", video.src);
  function progress(pct){
    console.log(pct);
  }


  const old_src = video.src;
  video.src = "";
  downloadToBlob(old_src, progress).then(url => video.src = url);
}

function createSpinner() {

  /** @type{(pct: number) => void}*/
  const updatePct = pct => {
    const pct_str = (pct * 10).toFixed(0);
    
  };

  return updatePct;
}


/**
Prefetch the video, return the fully fetched URL
 */
async function downloadToBlob(url, onProgress) {
  const response = await fetch(url);
  const content_length_header = response.headers.get('Content-Length');
  if (!content_length_header) return;
  const content_length = parseInt(content_length_header);
  if (isNaN(content_length) || content_length <= 0) return;
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
