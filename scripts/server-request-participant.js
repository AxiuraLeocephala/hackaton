document.addEventListener('DOMContentLoaded', () => {
    const participantForm = document.getElementById('participantForm');

    participantForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const participantData = {
            first_name: document.getElementById('first-name').value.trim(),
            second_name: document.getElementById('second-name').value.trim(),
            patronymic: document.getElementById('patronymic').value.trim(),
            age: parseInt(document.getElementById('athlete-age').value),
            name_team: document.getElementById('athlete-team').value.trim(),
        };

        try {
            const response = await fetch('https://ungraciously-gracious-surgeonfish.cloudpub.ru/registration_participant', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(participantData),
            });

            if (!response.ok) {
                const err = await response.text();
                throw new Error(`Ошибка: ${response.status} — ${err}`);
            }

            const result = await response.json();
            console.log('Ответ от сервера:', result);

            if (result.success) {
                alert('Участник успешно зарегистрирован!');
                participantForm.reset();
            } else {
                alert('Ошибка при регистрации участника');
            }
        } catch (error) {
            console.error('Ошибка при отправке:', error);
            alert('Не удалось отправить данные на сервер');
        }
    });
});
