const rotinas = JSON.parse(document.getElementById('rotinas-data').dataset.rotinas);

function formatarData(dateObj) {
    return dateObj.toLocaleDateString('pt-BR', { weekday: 'long', day: '2-digit', month: 'long', year: 'numeric' });
}

function openModal(dateStr, dayRotinas, dayFeriado) {
    const modal = document.getElementById('modal');
    const modalTitle = document.getElementById('modal-title');
    const modalBody = document.getElementById('modal-body');

    // Formata o título da data
    const [year, month, day] = dateStr.split('-').map(Number);
    const dateObj = new Date(year, month - 1, day);
    modalTitle.textContent = formatarData(dateObj);

    modalBody.innerHTML = '';

    // Feriado
    if (dayFeriado) {
        const feriadoEl = document.createElement('div');
        feriadoEl.classList.add('modal-feriado');
        feriadoEl.innerHTML = `🗓️ <strong>${dayFeriado.name}</strong> <span>(${dayFeriado.type})</span>`;
        modalBody.appendChild(feriadoEl);
    }

    // Rotinas do dia
    if (dayRotinas.length > 0) {
        dayRotinas.forEach(r => {
            const item = document.createElement('div');
            item.classList.add('modal-rotina');
            item.innerHTML = `
                <strong>${r.name}</strong>
                <span>⏰ ${r.startTime} - ${r.endTime}</span>
                ${r.description ? `<p>${r.description}</p>` : ''}
                <div class="modal-rotina__buttons">
                    <a href="/task/update/${r.id}" class="btn-modal-editar">Editar</a>
                    <form action="/task/delete/${r.id}" method="POST" onsubmit="return confirm('Excluir esta rotina?')">
                        <button type="submit" class="btn-modal-excluir">Excluir</button>
                    </form>
                </div>
            `;
            modalBody.appendChild(item);
        });
    } else if (!dayFeriado) {
        modalBody.innerHTML = '<p>Nenhuma rotina agendada para este dia.</p>';
    }

    modal.classList.add('modal--visible');
}

function closeModal() {
    document.getElementById('modal').classList.remove('modal--visible');
}

document.addEventListener('DOMContentLoaded', async function () {
    // Busca feriados antes de inicializar o calendário
    let feriadosPorData = {};
    try {
        const year = new Date().getFullYear();
        const resp = await fetch(`/task/feriados?year=${year}`);
        const feriados = await resp.json();
        feriados.forEach(f => { feriadosPorData[f.date] = f; });
    } catch (err) {
        console.warn('Não foi possível carregar feriados:', err);
    }

    // Agrupa rotinas por data
    const rotinasPorData = {};
    rotinas.forEach(r => {
        if (!rotinasPorData[r.date]) rotinasPorData[r.date] = [];
        rotinasPorData[r.date].push(r);
    });

    const calendarEl = document.getElementById('calendar');
    const calendar = new FullCalendar.Calendar(calendarEl, {
        locale: 'pt-br',
        initialView: 'dayGridMonth',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,listMonth'
        },
        dayCellDidMount: function (info) {
            const dateStr = info.date.toISOString().split('T')[0];
            const hasRotinas = rotinasPorData[dateStr];
            const hasFeriado = feriadosPorData[dateStr];

            if (hasRotinas || hasFeriado) {
                const dots = document.createElement('div');
                dots.classList.add('day-dots');
                if (hasRotinas) {
                    const d = document.createElement('span');
                    d.classList.add('dot', 'dot-rotina');
                    dots.appendChild(d);
                }
                if (hasFeriado) {
                    const d = document.createElement('span');
                    d.classList.add('dot', 'dot-feriado');
                    dots.appendChild(d);
                }
                const frame = info.el.querySelector('.fc-daygrid-day-frame');
                if (frame) frame.appendChild(dots);
                else info.el.appendChild(dots);
            }
        },
        dateClick: function (info) {
            const dayRotinas = rotinasPorData[info.dateStr] || [];
            const dayFeriado = feriadosPorData[info.dateStr] || null;
            openModal(info.dateStr, dayRotinas, dayFeriado);
        }
    });

    calendar.render();

    // Fecha modal ao clicar no overlay
    document.getElementById('modal').addEventListener('click', function (e) {
        if (e.target === this) closeModal();
    });
    document.getElementById('modal-close').addEventListener('click', closeModal);
});