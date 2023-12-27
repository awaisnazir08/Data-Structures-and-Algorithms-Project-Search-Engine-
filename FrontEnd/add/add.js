async function uploadFile() {
    const fileInput = document.getElementById("jsonFile");
    const processingDiv = document.getElementById("processing");
    const messagediv = document.getElementById("message");

    const file = fileInput.files[0];
    if (!file) {
      alert("Please select a JSON file.");
      return;
    }

    // Show processing message
    processingDiv.style.display = "block";

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://127.0.0.1:8000/add", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      if (response.status === 200) {
        messagediv.textContent =
          "Document inserted successfully in the search engine";
        messagediv.style.display = "block";
      } else if (response.status === 201) {
        messagediv.textContent =
          "This document is already present in the search engine. Try adding some other document or go ahead search for your queries.";
        messagediv.style.display = "block";
      } else if (response.status === 500) {
        messagediv.textContent =
          "Please select a valid file type. Only JSON files are allowed.";
        messagediv.style.display = "block";
      }
      console.log("Response Status:", response.status);

      console.log("File uploaded successfully! Response:", response.data);
    } catch (error) {
      console.error("Axios Error:", error);
    }
  }
