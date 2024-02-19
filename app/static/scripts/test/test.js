// script.js

// Function that simulates an asynchronous operation
function fetchData() {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve("Dynamic content loaded!");
        }, 2000); // Simulating a delay of 2 seconds
    });
}

// Function to update the DOM with dynamic content
async function updateDynamicContent() {
    const dynamicContentElement = document.getElementById("dynamic-content");

    try {
        const data = await fetchData();
        dynamicContentElement.textContent = data;
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

// Call the function to update dynamic content
updateDynamicContent();
