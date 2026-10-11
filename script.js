// ==================================================
// DOM Elements
// ==================================================

const chatForm = document.getElementById("chat-form");
const questionInput = document.getElementById("question-input");
const sendButton = document.getElementById("send-button");
const chatMessages = document.getElementById("chat-messages");
const loading = document.getElementById("loading");


// ==================================================
// Escape HTML
// Prevent unsafe HTML from API/database data
// ==================================================

function escapeHtml(value) {

    if (value === null || value === undefined) {
        return "";
    }

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


// ==================================================
// Add User Message
// ==================================================

function addUserMessage(question) {

    const message = document.createElement("div");

    message.className = "message user-message";

    message.innerHTML = `
        <div class="message-content">

            <div class="message-role">
                You
            </div>

            <p>
                ${escapeHtml(question)}
            </p>

        </div>
    `;

    chatMessages.appendChild(message);

    scrollToBottom();
}


// ==================================================
// Add Assistant Response
// ==================================================

function addAssistantMessage(data) {

    const sql = data.sql;
    const columns = data.columns || [];
    const rows = data.rows || [];

    let tableHtml = "";

    // ----------------------------------------------
    // Create result table
    // ----------------------------------------------

    if (columns.length > 0) {

        tableHtml = `
            <div class="result-table-container">

                <table class="result-table">

                    <thead>
                        <tr>
                            ${columns
                                .map(column => `
                                    <th>
                                        ${escapeHtml(column)}
                                    </th>
                                `)
                                .join("")
                            }
                        </tr>
                    </thead>

                    <tbody>

                        ${
                            rows.length > 0
                                ? rows.map(row => `
                                    <tr>
                                        ${
                                            row.map(value => `
                                                <td>
                                                    ${formatValue(value)}
                                                </td>
                                            `).join("")
                                        }
                                    </tr>
                                `).join("")
                                : `
                                    <tr>
                                        <td colspan="${columns.length}">
                                            No results found.
                                        </td>
                                    </tr>
                                `
                        }

                    </tbody>

                </table>

            </div>
        `;

    } else {

        tableHtml = `
            <p class="no-results">
                No result columns returned.
            </p>
        `;
    }


    // ----------------------------------------------
    // Create assistant message
    // ----------------------------------------------

    const message = document.createElement("div");

    message.className = "message assistant-message";

    message.innerHTML = `

        <div class="message-content">

            <div class="message-role">
                AI Assistant
            </div>

            <p>
                Here is the result for your question:
            </p>


            <!-- SQL Query -->

            <div class="sql-section">

                <div class="result-label">
                    Generated SQL
                </div>

                <pre class="sql-code"><code>${escapeHtml(sql)}</code></pre>

            </div>


            <!-- Query Result -->

            <div class="result-section">

                <div class="result-label">
                    Query Result
                </div>

                ${tableHtml}

            </div>

        </div>
    `;

    chatMessages.appendChild(message);

    scrollToBottom();
}


// ==================================================
// Format Values
// ==================================================

function formatValue(value) {

    if (value === null || value === undefined) {
        return "NULL";
    }

    if (typeof value === "object") {
        return escapeHtml(JSON.stringify(value));
    }

    return escapeHtml(value);
}


// ==================================================
// Add Error Message
// ==================================================

function addErrorMessage(messageText) {

    const message = document.createElement("div");

    message.className = "message assistant-message";

    message.innerHTML = `

        <div class="message-content">

            <div class="message-role">
                AI Assistant
            </div>

            <p>
                ❌ ${escapeHtml(messageText)}
            </p>

        </div>
    `;

    chatMessages.appendChild(message);

    scrollToBottom();
}


// ==================================================
// Show / Hide Loading
// ==================================================

function showLoading() {
    loading.classList.remove("hidden");
}

function hideLoading() {
    loading.classList.add("hidden");
}


// ==================================================
// Scroll Chat to Bottom
// ==================================================

function scrollToBottom() {

    chatMessages.scrollTop = chatMessages.scrollHeight;
}


// ==================================================
// Send Question to Flask API
// ==================================================

async function sendQuestion(question) {

    try {

        const response = await fetch("/api/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })

        });


        const result = await response.json();


        // ------------------------------------------
        // Handle API Error
        // ------------------------------------------

        if (!response.ok || result.status !== "success") {

            throw new Error(
                result.message || "Something went wrong."
            );
        }


        // ------------------------------------------
        // Display Assistant Response
        // ------------------------------------------

        addAssistantMessage(result.data);


    } catch (error) {

        console.error("Chat API Error:", error);

        addErrorMessage(
            error.message || "Unable to process your question."
        );

    }
}


// ==================================================
// Chat Form Submit
// ==================================================

chatForm.addEventListener("submit", async function (event) {

    event.preventDefault();


    const question = questionInput.value.trim();


    // ----------------------------------------------
    // Empty question
    // ----------------------------------------------

    if (!question) {
        return;
    }


    // ----------------------------------------------
    // Show user message
    // ----------------------------------------------

    addUserMessage(question);


    // Clear input
    questionInput.value = "";


    // ----------------------------------------------
    // Disable input while processing
    // ----------------------------------------------

    sendButton.disabled = true;
    questionInput.disabled = true;


    // Show loading
    showLoading();


    // ----------------------------------------------
    // Call Flask API
    // ----------------------------------------------

    await sendQuestion(question);


    // ----------------------------------------------
    // Enable input again
    // ----------------------------------------------

    hideLoading();

    sendButton.disabled = false;
    questionInput.disabled = false;

    questionInput.focus();

});


// ==================================================
// Example Questions
// ==================================================

const exampleQuestions = document.querySelectorAll(
    ".example-question"
);


exampleQuestions.forEach(function (element) {

    element.addEventListener("click", function () {

        questionInput.value = element.textContent.trim();

        questionInput.focus();

    });

});


// ==================================================
// Initial Focus
// ==================================================

questionInput.focus();