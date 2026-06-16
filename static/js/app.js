document.addEventListener('DOMContentLoaded', () => {
    
    // --- QUANTUM TOPOLOGICAL MESH CANVAS ENGINE ---
    const canvas = document.getElementById('quantum-mesh-canvas');
    const ctx = canvas.getContext('2d');
    
    let dots = [];
    const spacing = 55; // Grid point frequency density tracking
    let mouse = { x: null, y: null, targetRadius: 160 };

    function initMesh() {
        dots = [];
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        
        // Construct the geometric multi-dimensional grid layout matrix
        for (let x = 0; x < canvas.width + spacing; x += spacing) {
            for (let y = 0; y < canvas.height + spacing; y += spacing) {
                dots.push({
                    baseX: x, baseY: y,
                    currentX: x, currentY: y,
                    vx: 0, vy: 0
                });
            }
        }
    }

    window.addEventListener('resize', initMesh);
    window.addEventListener('mousemove', (e) => { mouse.x = e.clientX; mouse.y = e.clientY; });
    window.addEventListener('mouseout', () => { mouse.x = null; mouse.y = null; });
    initMesh();

    function renderQuantumMesh() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Vector mapping point alterations
        for (let i = 0; i < dots.length; i++) {
            let d = dots[i];
            let dxBase = d.baseX - d.currentX;
            let dyBase = d.baseY - d.currentY;
            
            // Native return elasticity equations
            d.vx += dxBase * 0.03; d.vy += dyBase * 0.03;
            
            if (mouse.x !== null && mouse.y !== null) {
                let dxMouse = mouse.x - d.currentX;
                let dyMouse = mouse.y - d.currentY;
                let distMouse = Math.sqrt(dxMouse * dxMouse + dyMouse * dyMouse);
                
                if (distMouse < mouse.targetRadius) {
                    // Physics pull matrix calculation metrics
                    let pullForce = (mouse.targetRadius - distMouse) / mouse.targetRadius;
                    d.vx -= dxMouse * pullForce * 0.08; d.vy -= dyMouse * pullForce * 0.08;
                }
            }

            // Apply friction dampening parameters and adjust values
            d.vx *= 0.82; d.vy *= 0.82;
            d.currentX += d.vx; d.currentY += d.vy;

            // Render subtle point reference markers
            ctx.beginPath();
            ctx.arc(d.currentX, d.currentY, 0.8, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(99, 102, 241, 0.12)';
            ctx.fill();
        }

        // Draw topological matrix connection paths
        ctx.beginPath();
        ctx.strokeStyle = 'rgba(99, 102, 241, 0.025)';
        ctx.lineWidth = 0.6;

        let rowsCount = Math.ceil(canvas.height / spacing) + 1;
        let colsCount = Math.ceil(canvas.width / spacing) + 1;

        for (let c = 0; c < colsCount; c++) {
            for (let r = 0; r < rowsCount; r++) {
                let index = c * rowsCount + r;
                if (index >= dots.length) continue;
                
                // Draw link lines to the right neighbor
                if (c < colsCount - 1) {
                    let rightIndex = (c + 1) * rowsCount + r;
                    if (rightIndex < dots.length) {
                        ctx.moveTo(dots[index].currentX, dots[index].currentY);
                        ctx.lineTo(dots[rightIndex].currentX, dots[rightIndex].currentY);
                    }
                }
                // Draw link lines to the lower neighbor
                if (r < rowsCount - 1) {
                    let lowerIndex = index + 1;
                    if (lowerIndex < dots.length) {
                        ctx.moveTo(dots[index].currentX, dots[index].currentY);
                        ctx.lineTo(dots[lowerIndex].currentX, dots[lowerIndex].currentY);
                    }
                }
            }
        }
        ctx.stroke();
        requestAnimationFrame(renderQuantumMesh);
    }
    renderQuantumMesh();

    // --- TAB INTERACTIVE MIGRATION VIEW CONTROLS ---
    const btnChat = document.getElementById('tab-chat');
    const btnArch = document.getElementById('tab-arch');
    const panelChat = document.getElementById('panel-chat-view');
    const panelArch = document.getElementById('panel-architecture-view');

    btnChat.addEventListener('click', () => {
        btnChat.classList.add('active', 'text-white'); btnChat.classList.remove('text-slate-400');
        btnArch.classList.remove('active', 'text-white'); btnArch.classList.add('text-slate-400');
        panelChat.classList.remove('hidden'); panelArch.classList.add('hidden');
    });

    btnArch.addEventListener('click', () => {
        btnArch.classList.add('active', 'text-white'); btnArch.classList.remove('text-slate-400');
        btnChat.classList.remove('active', 'text-white'); btnChat.classList.add('text-slate-400');
        panelArch.classList.remove('hidden'); panelChat.classList.add('hidden');
    });

    // --- ASYNC PIPELINE DATA NETWORK ACTIONS ---
    const pdfInput = document.getElementById('pdf-input');
    const userQuery = document.getElementById('user-query');
    const submitBtn = document.getElementById('submit-btn');
    const chatContainer = document.getElementById('chat-container');
    const statusBadge = document.getElementById('status-badge');
    const activeBorder = document.getElementById('active-pulse-border');

    pdfInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        document.getElementById('upload-default').classList.add('hidden');
        document.getElementById('upload-loader').classList.remove('hidden');

        const formData = new FormData();
        formData.append('pdf', file);

        try {
            const res = await fetch('/upload', { method: 'POST', body: formData });
            const data = await res.json();

            if (data.success) {
                statusBadge.innerHTML = `<span class="w-2 h-2 rounded-full bg-emerald-500 mr-2 shadow-[0_0_12px_#10b981]"></span> READY`;
                statusBadge.className = "px-4 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-[11px] font-semibold text-emerald-400 flex items-center tracking-wider";
                document.getElementById('info-filename').innerText = file.name;
                document.getElementById('file-info-card').classList.remove('hidden');
                
                userQuery.disabled = false; submitBtn.disabled = false;
                userQuery.placeholder = "Search document entities, metrics, parameters...";
                userQuery.focus();
            }
        } catch (err) {
            alert('Upload vector compilation fault.');
        } finally {
            document.getElementById('upload-loader').classList.add('hidden');
            document.getElementById('upload-default').classList.remove('hidden');
        }
    });

    document.getElementById('query-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const queryText = userQuery.value.trim();
        if (!queryText) return;

        appendMsgBubble('user', queryText);
        userQuery.value = '';
        
        document.getElementById('thinking-indicator').classList.remove('hidden');
        activeBorder.classList.add('pulse-border-active');
        chatContainer.scrollTop = chatContainer.scrollHeight;

        try {
            const res = await fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: queryText })
            });
            const data = await res.json();
            appendMsgBubble('ai', data.answer, data.sources);
        } catch (err) {
            appendMsgBubble('ai', 'Error establishing matrix response validation streams.');
        } finally {
            document.getElementById('thinking-indicator').classList.add('hidden');
            activeBorder.classList.remove('pulse-border-active');
        }
    });

    function appendMsgBubble(role, text, sources = []) {
        const welcome = document.getElementById('welcome-message');
        if(welcome) welcome.remove();

        const row = document.createElement('div');
        row.className = `flex space-x-4 fade-in-element ${role === 'user' ? 'justify-end' : ''}`;
        
        let sourceBlock = '';
        if (sources && sources.length > 0) {
            sourceBlock = `
                <div class="mt-3 pt-2.5 border-t border-white/5 text-[10px] text-slate-500">
                    <span class="text-indigo-400 font-semibold block mb-1"><i class="fa-solid fa-folder-open mr-1"></i> Grounded Context Reference:</span>
                    <p class="bg-[#020406]/50 p-2.5 rounded-lg border border-white/5 font-mono select-all text-slate-400 leading-relaxed">${escapeHtml(sources[0].substring(0, 200))}...</p>
                </div>`;
        }

        row.innerHTML = `
            <div class="flex space-x-3 ${role === 'user' ? 'flex-row-reverse space-x-reverse' : ''} max-w-[75%]">
                <div class="w-8 h-8 rounded-lg flex-shrink-0 flex items-center justify-center text-xs shadow-md
                    ${role === 'user' ? 'bg-indigo-600 text-white' : 'bg-white/5 text-indigo-400 border border-white/10'}">
                    <i class="fa-solid fa-${role === 'user' ? 'user-astronaut' : 'brain'}"></i>
                </div>
                <div class="p-4 rounded-2xl text-sm leading-relaxed backdrop-blur-md
                    ${role === 'user' ? 'bg-indigo-600 text-white shadow-xl shadow-indigo-600/10' : 'bg-white/[0.02] text-slate-300 border border-white/5'}">
                    <p class="whitespace-pre-wrap">${escapeHtml(text)}</p>
                    ${sourceBlock}
                </div>
            </div>`;
        
        chatContainer.appendChild(row);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function escapeHtml(str) {
        return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }
});