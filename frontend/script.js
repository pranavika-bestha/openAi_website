async function sendMessage() {
  const messageInput = document.getElementById("message");
  const replyText = document.getElementById("replyText");
  const message = messageInput.value;

  try {
    const res = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    const data = await res.json();
    replyText.textContent = data.reply;
  } catch (err) {
    replyText.textContent = "Error connecting to backend.";
    console.error(err);
  }
}
