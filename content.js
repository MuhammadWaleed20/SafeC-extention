document.addEventListener('paste', (event) => {
    const pastedText = (event.clipboardData || window.clipboardData).getData('text');
    if (!pastedText) return;

    // Stop the paste dead in its tracks
    event.preventDefault();
    event.stopPropagation();

    // Send the text to our background service worker
    chrome.runtime.sendMessage({ action: "scanText", text: pastedText }, (response) => {
        if (chrome.runtime.lastError || response.error) {
            console.error("Scanner Error. Is Python running?", chrome.runtime.lastError || response.error);
            return;
        }

        if (response.is_safe) {
            // If Python says it's safe, manually inject the text
            document.execCommand('insertText', false, pastedText);
        } else {
            // If Python detects a secret, alert the user
            alert(`🚨 BLOCKED BY PYTHON: ${response.detected} detected in your paste!`);
            console.warn(`Attempted to paste sensitive data: ${response.detected}`);
        }
    });
}, true);