// audio duration - client side utility for checking the audio file length - enforcing it  


export function probeDuration(file: File): Promise<number> {
   return new Promise((resolve, reject) => {
      const audio = document.createElement("audio");
      const url = URL.createObjectURL(file);

      audio.preload = "metadata";
      audio.src = url;

      audio.onloadedmetadata = () => {
        URL.revokeObjectURL(url);
        resolve(audio.duration);
      };

      audio.onerror = () => {
        URL.revokeObjectURL(url);
        reject(new Error("Could not read this file as audio."));
      }
   });
}


