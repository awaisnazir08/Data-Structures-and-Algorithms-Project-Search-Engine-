let currentPage = 1;
const resultsPerPage = 10;
let documents = [];

async function search() {
  const query = document.getElementById("searchQuery").value;
  const data = { query: query };
  try {
    documents = [];

    const startTime = performance.now();
    const response = await fetch("http://127.0.0.1:8000/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (response.status === 404) {

      const apiCalled = document.getElementById("apiCalled");
      apiCalled.style.display = "block";
      const resultsDiv = document.getElementById("results");
      resultsDiv.style.display = "none";
      const paginationDiv = document.getElementById("pagination");
      paginationDiv.style.display = "none";
      const timeDiv = document.getElementById("time_taken");
      const docs = document.getElementById("docs_shown");
      docs.style.display = "none";
      timeDiv.style.display = "none";
      apiCalled.textContent =
        "The word is not present in the dictionary\nTry searching for other words";
      return;
    }

    if (response.ok) {
      const responseData = await response.json();
      documents = responseData.documents || [];
      displayResultsPerPage(1);
      const flexx = document.getElementById("flexx");
      flexx.style.display="flex";
      const resultsDiv = document.getElementById("results");
      resultsDiv.style.display = "block";
      const apiCalled = document.getElementById("apiCalled");
      apiCalled.style.display = "none";
      const endTime = performance.now();
      const timeTaken = endTime - startTime;
      const docs_shown = responseData.number;
      const t = responseData.execution_time;
      const total = timeTaken+t;
      const timeDiv = document.getElementById("time_taken");
      timeDiv.textContent = `Time taken: ${total.toFixed(2)} ms`;
      const docs = document.getElementById("docs_shown");
      docs.textContent = `Documents Shown: ${docs_shown}`; // Display number of documents shown
      docs.style.display = "block";
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
    const documentUrl = documentData.document_url || "#";

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
