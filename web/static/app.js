/**
 * NE-AI V1 — Frontend JS
 * -----------------------
 * Gerencia interações com backend:
 * - Memória
 * - Uploads (texto e arquivo)
 * - Execução de intenções
 * - Streaming
 * - Feedback humano
 */

// ==============================
// Atualiza memória aprendida
// ==============================
async function updateMemory() {
    try {
        const response = await fetch('/memory'); // Endpoint backend que retorna JSON
        const data = await response.json();
        const container = document.getElementById('memory_container');
        container.innerHTML = '';

        // Itera cada item da memória e cria div para exibição
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
    } catch (error) {
        console.error("[app.js] Falha ao atualizar memória:", error);
    }
}

// ==============================
// Envia texto para aprendizado
// ==============================
async function uploadText() {
    const text = document.getElementById('text_input').value;
    if (!text) return alert("Digite algo antes de enviar");

    await fetch('/upload_text', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: `text=${encodeURIComponent(text)}`
    });

    document.getElementById('text_input').value = '';
    updateMemory();
}

// ==============================
// Envia arquivo (imagem ou vídeo)
// ==============================
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

// ==============================
// Executa intenção baseada em texto
// ==============================
async function executeIntent() {
    const text = document.getElementById('text_input').value;
    if (!text) return alert("Digite algo para executar");

    await fetch('/execute_intent', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: `text=${encodeURIComponent(text)}`
    });

    document.getElementById('text_input').value = '';
    updateMemory();
}

// ==============================
// Comando genérico (ex: iniciar/parar streaming)
// ==============================
async function executeCommand(cmd) {
    await fetch('/execute_intent', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: `text=${encodeURIComponent(cmd)}`
    });

    // Atualiza status (podemos adicionar retorno do backend em breve)
    document.getElementById('status').innerText = `Último comando: ${cmd}`;
}

// ==============================
// Feedback humano sobre aprendizado
// ==============================
async function sendFeedback(id, positive) {
    await fetch('/feedback', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: `id=${encodeURIComponent(id)}&positive=${positive}`
    });

    updateMemory();
}

// ==============================
// Atualização periódica da memória
// ==============================
setInterval(updateMemory, 3000);  // Atualiza a cada 3 segundos
updateMemory();                   // Primeira atualização imediata
