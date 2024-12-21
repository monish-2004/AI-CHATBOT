document.getElementById("send-btn").addEventListener("click", () => {
    // Get user input from the text box
    const userInput = document.getElementById("user-input").value;

    // Prevent sending empty messages
    if (userInput.trim() === "") return;

    // Append the user message to the chat box
    const chatBox = document.getElementById("chat-box");
    const userMessage = document.createElement("div");
    userMessage.textContent = "You: " + userInput;
    chatBox.appendChild(userMessage);

    // Send the user message to the backend via a POST request
    fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userInput }),
    })
        .then((response) => response.json())
        .then((data) => {
            // Check if the response contains a valid 'response' property
            if (data && data.response) {
                // Create a bot message element and append it to the chat box
                const botMessage = document.createElement("div");
                botMessage.textContent = "Bot: " + data.response;
                chatBox.appendChild(botMessage);
            } else {
                console.error("Invalid response structure:", data);
            }
        })
        .catch((error) => {
            console.error("Error:", error);
        });

    // Clear the input field after sending the message
    document.getElementById("user-input").value = "";
});
