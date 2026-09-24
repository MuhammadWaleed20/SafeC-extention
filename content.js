document.addEventListener('paste', (event) => {
    const pastedText = (event.clipboardData || window.clipboardData).getData('text');
    if (!pastedText) return;

    // 1. Remember exactly which text box the user is typing in before we stop the paste
    const activeElement = document.activeElement;

    event.preventDefault();
    event.stopPropagation();

    chrome.runtime.sendMessage({ action: "scanText", text: pastedText }, (response) => {
        if (chrome.runtime.lastError || response.error) {
            console.error("Scanner Error. Is Python running?", chrome.runtime.lastError || response.error);
            return;
        }

        // 2. Safely inject the sanitized text into modern web apps (like ChatGPT)
        if (activeElement && (activeElement.tagName === 'TEXTAREA' || activeElement.tagName === 'INPUT')) {
            // Find where the blinking cursor is
            const start = activeElement.selectionStart;
            const end = activeElement.selectionEnd;

            // Slice the text in exactly at the cursor
            activeElement.value = activeElement.value.substring(0, start) + response.sanitized_text + activeElement.value.substring(end);

            // Move the cursor to the end of the newly pasted text
            activeElement.selectionStart = activeElement.selectionEnd = start + response.sanitized_text.length;

            // 3. Force React to notice the new text
            activeElement.dispatchEvent(new Event('input', { bubbles: true }));
        } else {
            // Fallback for older websites
            activeElement.focus();
            document.execCommand('insertText', false, response.sanitized_text);
        }

        if (response.was_redacted) {
            console.warn(`Secret Guardian protected you! Hid the following keys: ${response.detected.join(", ")}`);
        }
    });
}, true);