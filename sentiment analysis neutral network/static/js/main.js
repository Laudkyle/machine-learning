document.addEventListener("DOMContentLoaded", () => {
  const startRecordingBtn = document.getElementById("start-recording");
  const stopRecordingBtn = document.getElementById("stop-recording");
  const fileInput = document.getElementById("audio-file-input");
  const transcriptionContainer = document.getElementById("transcription");
  const sentimentContainer = document.getElementById("sentiment");
  const loadingContainer = document.getElementById("loading-container"); // Added loading container
  let recognition;

  // Check if the browser supports the Web Speech API
  if ("SpeechRecognition" in window || "webkitSpeechRecognition" in window) {
    recognition = new (window.SpeechRecognition ||
      window.webkitSpeechRecognition)();

    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onstart = () => {
      console.log("Recording started");
    };

    recognition.onresult = (event) => {
      const transcript = Array.from(event.results)
        .map((result) => result[0].transcript)
        .join("");

      transcriptionContainer.textContent = transcript;
    };

    recognition.onerror = (event) => {
      console.error("Speech recognition error:", event.error);
      console.log("Additional details:", event);
      stopRecording();
    };

    recognition.onend = () => {
      console.log("Recording ended");
    };

    startRecordingBtn.addEventListener("click", () => {
      startRecordingBtn.disabled = true;
      stopRecordingBtn.disabled = false;
      fileInput.disabled = true; // Disable file input during recording
      startRecording();
    });

    stopRecordingBtn.addEventListener("click", () => {
      startRecordingBtn.disabled = false;
      stopRecordingBtn.disabled = true;
      fileInput.disabled = false; // Enable file input after recording
      stopRecording();
    });
  } else {
    // Web Speech API is not supported
    console.error("Web Speech API is not supported in this browser.");
    startRecordingBtn.disabled = true;
    stopRecordingBtn.disabled = true;
    fileInput.disabled = true;
  }

  // Listen for file input change
  fileInput.addEventListener("change", handleFileSelect);

  function handleFileSelect(event) {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      // Disable recording buttons when a file is selected
      startRecordingBtn.disabled = true;
      stopRecordingBtn.disabled = true;

      // Show loading spinner
      showLoading();

      // Perform sentiment analysis using the backend server
      predictSentimentFromFile(selectedFile);
    }
  }

  async function startRecording() {
    if (recognition) {
      transcriptionContainer.textContent = "";
      recognition.start();
    }
  }

  async function stopRecording() {
    if (recognition) {
      recognition.stop();
    }

    // Get the transcribed text
    const transcribedText = transcriptionContainer.textContent;

    // Perform sentiment analysis using the backend server
    const predictedSentiment = await predictSentimentFromServer(
      transcribedText
    );

    // Display the predicted sentiment
    sentimentContainer.textContent = `Predicted Sentiment: ${predictedSentiment}`;

    // Show the overlay
    showOverlay(predictedSentiment);
  }

  async function showOverlay(sentiment) {
    const overlay = document.getElementById("prediction-overlay");
    const overlaySentiment = document.getElementById("overlay-sentiment");
    const emojiOverlay = document.getElementById("emoji-overlay");

    // Set the sentiment in the overlay
    overlaySentiment.textContent = sentiment;

    // Clear previous emoji content
    emojiOverlay.innerHTML = "";

    // Embed the appropriate emoji in the overlay
    if (sentiment === "Satisfied") {
      emojiOverlay.innerHTML =
        '<div class="tenor-gif-embed" data-postid="27588755" data-aspect-ratio="1.31687" data-width="300px"></div>';
    } else if (sentiment === "Neutral") {
      emojiOverlay.innerHTML =
        '<div class="tenor-gif-embed" data-postid="15341778" data-aspect-ratio="1.31687" data-width="300px"></div>';
    } else if (sentiment === "Unhappy") {
      emojiOverlay.innerHTML =
        '<div class="tenor-gif-embed" data-postid="18532170" data-aspect-ratio="1.31687" data-width="300px"></div>';
    }

    // Reload Tenor GIF script to render the new GIFs
    const script = document.createElement("script");
    script.type = "text/javascript";
    script.async = true;
    script.src = "https://tenor.com/embed.js";
    emojiOverlay.appendChild(script);

    // Display the overlay
    overlay.classList.remove("hidden");
  }

  async function showLoading() {
    loadingContainer.style.display = "block";
  }

  async function hideLoading() {
    loadingContainer.style.display = "none";
  }

  async function predictSentimentFromServer(text) {
    try {
      const formData = new FormData();
      formData.append("text", text); 

      const response = await fetch("/analyze", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server returned status ${response.status}`);
      }
      const data = await response.json();
      const emojiContainer = document.getElementById("emoji");
      emojiContainer.innerHTML = ""; // Reset content

      if (data.sentiment === "Satisfied") {
        // Embed the Happy GIF
        emojiContainer.innerHTML =
          '<div class="tenor-gif-embed" data-postid="27588755" data-aspect-ratio="1.31687" data-width="300px"></div>';
      } else if (data.sentiment === "Neutral") {
        // Embed the Neutral GIF
        emojiContainer.innerHTML =
          '<div class="tenor-gif-embed" data-postid="15341778" data-aspect-ratio="1.31687" data-width="300px"></div>';
      } else if (data.sentiment === "Unhappy") {
        // Embed the Unhappy GIF
        emojiContainer.innerHTML =
          '<div class="tenor-gif-embed" data-postid="18532170" data-aspect-ratio="1.31687" data-width="300px"></div>';
      }

      // Reload Tenor GIF script to render the new GIFs
      const script = document.createElement("script");
      script.type = "text/javascript";
      script.async = true;
      script.src = "https://tenor.com/embed.js";
      emojiContainer.appendChild(script);

      return data.sentiment;
    } catch (error) {
      console.error("Error during sentiment prediction:", error.message);
      return "Unknown";
    }
  }

  async function predictSentimentFromFile(audioFile) {
    try {
      const formData = new FormData();
      formData.append("audio", audioFile);

      const response = await fetch("/analyze", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        console.log(response);
        throw new Error(`Server returned status ${response.status}`);
      }

      const data = await response.json();
      const emojiContainer = document.getElementById("emoji");
      emojiContainer.innerHTML = ""; // Reset content

      if (data.sentiment === "Satisfied") {
        // Embed the Happy GIF
        emojiContainer.innerHTML =
          '<div class="tenor-gif-embed" data-postid="27588755" data-aspect-ratio="1.31687" data-width="300px"></div>';
      } else if (data.sentiment === "Neutral") {
        // Embed the Neutral GIF
        emojiContainer.innerHTML =
          '<div class="tenor-gif-embed" data-postid="15341778" data-aspect-ratio="1.31687" data-width="300px"></div>';
      } else if (data.sentiment === "Unhappy") {
        // Embed the Unhappy GIF
        emojiContainer.innerHTML =
          '<div class="tenor-gif-embed" data-postid="18532170" data-aspect-ratio="1.31687" data-width="300px"></div>';
      }

      // Reload Tenor GIF script to render the new GIFs
      const script = document.createElement("script");
      script.type = "text/javascript";
      script.async = true;
      script.src = "https://tenor.com/embed.js";
      emojiContainer.appendChild(script);
      sentimentContainer.textContent = `Predicted Sentiment: ${data.sentiment}`;
    } catch (error) {
      console.error("Error during sentiment prediction:", error.message);
      sentimentContainer.textContent = "Unknown";
    } finally {
      // Hide loading spinner after the analysis is done
      hideLoading();
    }
  }
});
