document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    if (!calendarEl) return;

    var eventsUrl = calendarEl.dataset.eventsUrl;
    var prontuarioUrlBase = calendarEl.dataset.prontuarioUrl.slice(0, -1); 
    // var whatsappUrlBase = calendarEl.dataset.whatsappUrl.slice(0, -1); // Não vamos mais usar a API simulada

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'pt-br',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: eventsUrl,
        themeSystem: 'bootstrap5',
        height: 700,
        slotMinTime: '08:00:00',
        slotMaxTime: '20:00:00',
        allDaySlot: false,
        eventClick: function(info) {
            openEventDetails(info.event);
        }
    });
    calendar.render();

    // Modal Logic
    const eventModalEl = document.getElementById('eventModal');
    const eventModal = new bootstrap.Modal(eventModalEl);

    function openEventDetails(event) {
        // Preencher dados básicos
        document.getElementById('currentEventId').value = event.id;
        
        const clientName = event.title.split(' - ')[0];
        document.getElementById('eventCliente').innerText = clientName; 
        document.getElementById('eventServico').innerText = event.extendedProps.servico || 'Serviço';
        document.getElementById('eventTelefone').innerText = event.extendedProps.telefone || 'Sem telefone';
        document.getElementById('eventEmail').innerText = event.extendedProps.email || 'Sem email';
        
        const start = event.start.toLocaleString('pt-BR', { dateStyle: 'short', timeStyle: 'short' });
        document.getElementById('eventHorario').innerText = start;

        // Armazenar dados para o botão do WhatsApp
        eventModalEl.dataset.phone = event.extendedProps.telefone || '';
        eventModalEl.dataset.client = clientName;
        eventModalEl.dataset.service = event.extendedProps.servico || '';
        eventModalEl.dataset.date = start;

        // Carregar Prontuário
        loadProntuario(event.id);
        
        eventModal.show();
    }

    window.loadProntuario = function(id) {
        // Limpar campos
        document.getElementById('prontuarioQueixa').value = '';
        document.getElementById('prontuarioHistorico').value = '';
        document.getElementById('prontuarioObservacoes').value = '';

        fetch(prontuarioUrlBase + id)
            .then(res => res.json())
            .then(data => {
                if (data.queixa) document.getElementById('prontuarioQueixa').value = data.queixa;
                if (data.historico) document.getElementById('prontuarioHistorico').value = data.historico;
                if (data.observacoes) document.getElementById('prontuarioObservacoes').value = data.observacoes;
            });
    }

    window.saveProntuario = function() {
        const id = document.getElementById('currentEventId').value;
        const formData = new FormData(document.getElementById('prontuarioForm'));

        fetch(prontuarioUrlBase + id, {
            method: 'POST',
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert('Prontuário salvo com sucesso!');
            } else {
                alert('Erro ao salvar.');
            }
        });
    }

    window.sendWhatsappReminder = function() {
        const modal = document.getElementById('eventModal');
        let phone = modal.dataset.phone;
        const client = modal.dataset.client;
        const service = modal.dataset.service;
        const date = modal.dataset.date;

        // Limpeza simples do telefone
        phone = phone.replace(/\D/g, '');

        if (!phone) {
            alert('Este agendamento não possui um telefone cadastrado para envio.');
            return;
        }

        // Adicionar código do país se não houver (assumindo BR)
        if (phone.length <= 11) {
            phone = '55' + phone;
        }

        const message = `Olá ${client}, lembramos do seu agendamento de *${service}* para o dia *${date}*. \nPodemos confirmar?`;
        const url = `https://wa.me/${phone}?text=${encodeURIComponent(message)}`;
        
        // Abrir em nova aba
        window.open(url, '_blank');
    }
});
