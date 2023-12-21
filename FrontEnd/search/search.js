let currentPage = 1;
const resultsPerPage = 10;
let documents = [];
let documentUrls = {};

async function search() {
  const query = document.getElementById("searchQuery").value;
  const data = { query: query };


  try {
    const startTime = performance.now();
    const response = await fetch("http://127.0.0.1:5000/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (response.status === 401) {
      const apiCalled = document.getElementById("apiCalled");
      apiCalled.style.display = "block";
      apiCalled.textContent = "No such word found in the dictionary.";
      return;
    }
    if (response.status === 402) {
      const apiCalled = document.getElementById("apiCalled");
      apiCalled.style.display = "block";
      apiCalled.textContent = "Searched query is not present in any document";
      return;
    }
    if (response.ok) {
      const responseData = await response.json();
      console.log(responseData);
      documents = responseData.documents || [];
      documentUrls = responseData.document_url || {};
      displayResultsPerPage(1);

      const resultsDiv = document.getElementById("results");
      resultsDiv.style.display = "block";
      const apiCalled = document.getElementById("apiCalled");
      apiCalled.style.display = "none";
      const endTime = performance.now();
      const timeTaken = endTime - startTime;
      const timeDiv = document.getElementById("time_taken");
      timeDiv.textContent = `Time taken: ${timeTaken.toFixed(2)} milliseconds`;
    } else {
      console.error(
        "There was a problem with the fetch operation:",
        response.statusText
      );
    }
  } catch (error) {
    console.error("Error:", error);
  }
  currentPage = 1;
}

function displayResultsPerPage(page) {
    const startIdx = (page - 1) * resultsPerPage;
    const endIdx = startIdx + resultsPerPage;
    const totalResults = documents.length;

    const slicedResults = documents.slice(startIdx, endIdx);

    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";

    slicedResults.forEach((documentData) => {
      const documentId = documentData[1]; // Accessing the document ID from the nested array
      const documentUrl = documentUrls[documentId] || "#";

      const documentDiv = document.createElement("div");
      documentDiv.classList.add("search-result");

      const urlAnchor = document.createElement("a");
      urlAnchor.textContent = documentUrl;
      urlAnchor.href = documentUrl;
      urlAnchor.target = "_blank";

      const urlParagraph = document.createElement("p");
      urlParagraph.appendChild(urlAnchor);

      documentDiv.appendChild(urlParagraph);
      resultsDiv.appendChild(documentDiv);
    });

    const paginationDiv = document.getElementById("pagination");
    paginationDiv.style.display = "block";

    const currentPageSpan = document.getElementById("currentPage");
    currentPageSpan.textContent = `Page: ${currentPage} / ${Math.ceil(
      totalResults / resultsPerPage
    )}`;
  }
function nextPage() {
  const totalPages = Math.ceil(documents.length / resultsPerPage);
  if (currentPage < totalPages) {
    currentPage++;
    displayResultsPerPage(currentPage);
  }
}

function prevPage() {
  if (currentPage > 1) {
    currentPage--;
    displayResultsPerPage(currentPage);
  }
}

// Initial call to search function or bind it to a button click event
// search();
