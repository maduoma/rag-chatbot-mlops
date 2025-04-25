// app/ui/static/js/editor.js

document.addEventListener("DOMContentLoaded", () => {
    const resendButtons = document.querySelectorAll(".resend-btn");

    resendButtons.forEach(btn => {
        btn.addEventListener("click", async (e) => {
            const container = btn.closest(".message");
            const messageId = container.dataset.messageId;
            const newQuery = container.textContent.trim();

            // Remove button text from query
            const cleanQuery = newQuery.replace("✎", "").replace("↻", "").trim();

            const response = await fetch("/resend", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message_id: parseInt(messageId), query: cleanQuery })
            });

            const result = await response.json();
            if (result.success) {
                // replace content visually and enable toggling
                const botDiv = container.nextElementSibling;
                const prev = botDiv.innerText;
                const toggle = botDiv.querySelector(".toggle-history");
                toggle.style.display = "inline-block";

                botDiv.dataset.original = prev;
                botDiv.dataset.current = result.new_answer;
                botDiv.innerText = result.new_answer;

                // Add back the copy icon
                const copyIcon = document.createElement("span");
                copyIcon.className = "copy-icon";
                copyIcon.title = "Copy";
                copyIcon.innerHTML = "📋";
                botDiv.appendChild(copyIcon);
            }
        });
    });

    const toggleButtons = document.querySelectorAll(".toggle-history button");

    toggleButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const bot = btn.closest(".message");
            if (btn.classList.contains("toggle-previous")) {
                bot.innerText = bot.dataset.original;
            } else {
                bot.innerText = bot.dataset.current;
            }
        });
    });

    // Editable user query logic
    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const bubble = btn.closest('.gpt-bubble-user');
            bubble.querySelector('.gpt-user-text').style.display = 'none';
            btn.style.display = 'none';
            bubble.querySelector('.edit-area').style.display = 'flex';
            bubble.querySelector('.edit-textarea').focus();
        });
    });

    document.querySelectorAll('.cancel-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const bubble = btn.closest('.gpt-bubble-user');
            bubble.querySelector('.edit-area').style.display = 'none';
            bubble.querySelector('.gpt-user-text').style.display = '';
            bubble.querySelector('.edit-btn').style.display = '';
        });
    });

    document.querySelectorAll('.resend-btn').forEach(btn => {
        btn.addEventListener('click', async function () {
            const bubble = btn.closest('.gpt-bubble-user');
            const messageDiv = bubble.closest('.message.user');
            const textarea = bubble.querySelector('.edit-textarea');
            const newQuery = textarea.value.trim();
            const messageId = messageDiv.dataset.messageId;
            if (!newQuery) return;
            // Call /resend endpoint
            const response = await fetch('/resend', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message_id: parseInt(messageId), query: newQuery })
            });
            const result = await response.json();
            if (result.success) {
                bubble.querySelector('.gpt-user-text').textContent = newQuery;
                bubble.querySelector('.edit-area').style.display = 'none';
                bubble.querySelector('.gpt-user-text').style.display = '';
                bubble.querySelector('.edit-btn').style.display = '';
                // Optionally reload to show updated bot response
                window.location.reload();
            }
        });
    });
});