document.getElementById('jsonFile').addEventListener('change', function() {
  const fileInput = document.getElementById('jsonFile');
  const fileLabel = document.getElementById('fileLabel');

  if (fileInput.files.length > 0) {
    fileLabel.textContent = fileInput.files[0].name; // Display the chosen file name
  } else {
    fileLabel.textContent = 'Choose a file...';
  }
});


async function uploadFile() {
  const fileInput = document.getElementById("jsonFile");
  const processingDiv = document.getElementById("processing");
  const messagediv = document.getElementById("message");

  const file = fileInput.files[0];
  if (!file) {
    alert("Please select a JSON file.");
    return;
  }

  processingDiv.style.display = "block";

  const formData = new FormData();
  formData.append("file", file);

  try {
  console.log("api call hogayi")
    const response = await fetch("http://127.0.0.1:8000/add", {
      method: "POST",
      body: formData,
    });
    console.log("here");

    if (response.status === 200) {
      messagediv.textContent = "Document inserted successfully in the search engine";
      return;
    } else if (response.status === 201) {
      messagediv.textContent = "This document is already present in the search engine. Try adding some other document or go ahead search for your queries.";
      return;
    } else {
      messagediv.textContent = "Unexpected response from server.";
      return;
    }
    messagediv.style.display = "block";
  } catch (error) {
    console.error("Fetch Error:", error.message);
    messagediv.textContent = `Error: ${error.message}. Please try again.`;
    messagediv.style.display = "block";
  }
}
