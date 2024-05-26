// CSRF token'ı tüm AJAX isteklerine ekle
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function updateExplanationCounts(explanationId, upvotes, downvotes, favorites) {
    document.querySelectorAll(`[data-id='${explanationId}'] .upvote-count`).forEach(el => el.textContent = upvotes);
    document.querySelectorAll(`[data-id='${explanationId}'] .downvote-count`).forEach(el => el.textContent = downvotes);
    document.querySelectorAll(`[data-id='${explanationId}'] .favorite-count`).forEach(el => el.textContent = favorites);
    document.querySelectorAll(`[data-id='${explanationId}'] .total-votes`).forEach(el => el.textContent = upvotes - downvotes);
}

function updateButtonState(button, state, addedClass, removedClass) {
    if (state === 'added') {
        button.querySelector('i').classList.add(addedClass);
        button.querySelector('i').classList.remove(removedClass);
    } else {
        button.querySelector('i').classList.remove(addedClass);
        button.querySelector('i').classList.add(removedClass);
    }
}

document.querySelectorAll('.upvote-btn').forEach(button => {
    button.addEventListener('click', () => {
        const explanationId = button.getAttribute('data-id');
        fetch(`/explanation/${explanationId}/upvote/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json',
            }
        }).then(response => response.json()).then(data => {
            if (data.status === 'self_vote') {
                alert(data.message);
            } else {
                updateExplanationCounts(explanationId, data.total_up_votes, data.total_down_votes, data.total_favorites);
                updateButtonState(button, data.status, 'text-blue-500', 'text-gray-500');
            }
        });
    });
});

document.querySelectorAll('.downvote-btn').forEach(button => {
    button.addEventListener('click', () => {
        const explanationId = button.getAttribute('data-id');
        fetch(`/explanation/${explanationId}/downvote/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json',
            }
        }).then(response => response.json()).then(data => {
            if (data.status === 'self_vote') {
                alert(data.message);
            } else {
                updateExplanationCounts(explanationId, data.total_up_votes, data.total_down_votes, data.total_favorites);
                updateButtonState(button, data.status, 'text-red-500', 'text-gray-500');
            }
        });
    });
});

document.querySelectorAll('.favorite-btn').forEach(button => {
    button.addEventListener('click', () => {
        const explanationId = button.getAttribute('data-id');
        fetch(`/explanation/${explanationId}/favorite/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json',
            }
        }).then(response => response.json()).then(data => {
            if (data.status === 'self_favorite') {
                alert(data.message);
            } else {
                updateExplanationCounts(explanationId, data.total_up_votes, data.total_down_votes, data.total_favorites);
                updateButtonState(button, data.status, 'text-red-500', 'text-gray-500');
            }
        });
    });
});
