/* ============================================================
   script.js — SDU Sistema de Denúncias Urbanas
   Funções compartilhadas entre todas as páginas.
   ============================================================ */

// ── SIDEBAR ──────────────────────────────────────────────────
const sidebar      = document.getElementById("sidebar");
const menuToggle   = document.getElementById("menuToggle");

if (sidebar) {

    // Clique no botão hambúrguer → recolhe (sidebar aberta)
    if (menuToggle) {
        menuToggle.addEventListener("click", (e) => {
            e.stopPropagation(); // não dispara o listener da sidebar
            sidebar.classList.add("collapsed");
        });
    }

    // Clique em qualquer lugar da sidebar → expande (sidebar recolhida)
    sidebar.addEventListener("click", () => {
        if (sidebar.classList.contains("collapsed")) {
            sidebar.classList.remove("collapsed");
        }
    });

    // Impede que cliques nos itens do menu também disparem o toggle
    sidebar.querySelectorAll(".menu-item").forEach(item => {
        item.addEventListener("click", (e) => {
            e.stopPropagation();
        });
    });
}


// ── TOAST (notificação rápida) ───────────────────────────────
/**
 * Exibe uma mensagem temporária no canto inferior direito.
 * @param {string} msg    - Texto da mensagem.
 * @param {number} duracao - Tempo em ms (padrão: 3000).
 */
function mostrarToast(msg, duracao = 3000) {
    let toast = document.getElementById("toast");

    // Cria o elemento se ainda não existir
    if (!toast) {
        toast = document.createElement("div");
        toast.id = "toast";
        toast.className = "toast";
        document.body.appendChild(toast);
    }

    toast.textContent = msg;
    toast.classList.add("mostrar");

    setTimeout(() => {
        toast.classList.remove("mostrar");
    }, duracao);
}


// ── UTILITÁRIOS DE API ───────────────────────────────────────
const API = "http://127.0.0.1:5000";

/**
 * Busca todas as denúncias da API.
 * @returns {Promise<Array>} Lista de denúncias.
 */
async function buscarDenuncias() {
    const resposta = await fetch(`${API}/denuncias`);
    if (!resposta.ok) throw new Error("Erro ao buscar denúncias.");
    return resposta.json();
}

/**
 * Cria uma nova denúncia.
 * @param {Object} dados - Campos da denúncia.
 */
async function criarDenuncia(dados) {
    const resposta = await fetch(`${API}/denuncias`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados),
    });
    if (!resposta.ok) {
        const erro = await resposta.json();
        throw new Error(erro.erro || "Erro ao criar denúncia.");
    }
    return resposta.json();
}

/**
 * Atualiza campos de uma denúncia existente.
 * @param {number} id    - ID da denúncia.
 * @param {Object} dados - Campos a atualizar.
 */
async function atualizarDenuncia(id, dados) {
    const resposta = await fetch(`${API}/denuncias/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados),
    });
    if (!resposta.ok) throw new Error("Erro ao atualizar denúncia.");
    return resposta.json();
}

/**
 * Exclui uma denúncia.
 * @param {number} id - ID da denúncia.
 */
async function excluirDenuncia(id) {
    const resposta = await fetch(`${API}/denuncias/${id}`, {
        method: "DELETE",
    });
    if (!resposta.ok) throw new Error("Erro ao excluir denúncia.");
    return resposta.json();
}
