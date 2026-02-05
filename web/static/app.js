// Função para atualizar a memória
async function updateMemory() {
    const response = await fetch('/memory');
    const data = await response.json();
    const container = document.getElementById('memory_container');
    container.innerHTML = '';
    data.forEach(item => {
        const div = document.createElement('div');
        div.className = 'memory-item';
        div.innerHTML = `<b>ID:</b> ${item.id}<br>
                         <b>Tipo:</b> ${item.type}<br>
                         <b>Conteúdo:</b> ${item.content}<br>
                         <b>Confiança:</b> ${item.confidence.toFixed(2)}<br>
                         <b>Relevância:</b> ${item.relevance.toFixed(2)}<br>
                         <b>Visualizações:</b> ${item.times_seen}
                         <button class="feedback-btn" onclick="sendFeedback('${item.id}', true)">👍</button>
                         <button class="feedback-btn" onclick="sendFeedback('${item.id}', false)">👎</button>`;
        container.appendChild(div);
    });
}

// Envia texto para aprendizado
async function uploadText() {
    const text = document.getElementById('text_input').value;
    if (!text) return alert("Digite algo");
    await fetch('/upload_text', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: `text=${encodeURIComponent(text)}`
    });
    document.getElementById('text_input').value = '';
    updateMemory();
}

// Envia arquivo (imagem ou vídeo)
async function uploadFile() {
    const fileInput = document.getElementById('file_input');
    if (fileInput.files.length === 0) return alert("Selecione um arquivo");
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);
    await fetch('/upload_file', { method: 'POST', body: formData });
    fileInput.value = '';
    updateMemory();
}

// Executa intenção baseada no texto
async function executeIntent() {
    const text = document.getElementById('text_input').value;
    if (!text) return alert("Digite algo");
    await fetch('/execute_intent', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: `text=${encodeURIComponent(text)}`
    });
    document.getElementById('text_input').value = '';
    updateMemory();
}

// Comando genérico para iniciar/parar streaming
async function executeCommand(cmd) {
    await fetch('/execute_intent', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: `text=${encodeURIComponent(cmd)}`
    });
}

// Feedback humano
async function sendFeedback(id, positive) {
    await fetch('/feedback', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: `id=${encodeURIComponent(id)}&positive=${positive}`
    });
    updateMemory();
}

// Atualiza memória periodicamente
setInterval(updateMemory, 3000);
updateMemory();
