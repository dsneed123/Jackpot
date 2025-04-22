const list = document.getElementById('bucket-list');
let draggingEle;
let placeholder;
let isDraggingStarted = false;

const mouseDownHandler = function (e) {
    draggingEle = e.target;
    placeholder = document.createElement('li');
    placeholder.className = 'draggable placeholder';
    draggingEle.parentNode.insertBefore(placeholder, draggingEle.nextSibling);
    draggingEle.classList.add('dragging');
    isDraggingStarted = true;

    document.addEventListener('mousemove', mouseMoveHandler);
    document.addEventListener('mouseup', mouseUpHandler);
};

const mouseMoveHandler = function (e) {
    if (!isDraggingStarted) return;
    const draggingRect = draggingEle.getBoundingClientRect();
    draggingEle.style.position = 'absolute';
    draggingEle.style.top = `${e.clientY - draggingRect.height / 2}px`;
    draggingEle.style.left = `${e.clientX - draggingRect.width / 2}px`;

    const prevEle = draggingEle.previousElementSibling;
    const nextEle = placeholder.nextElementSibling;

    if (prevEle && isAbove(draggingEle, prevEle)) {
        swap(placeholder, prevEle);
    } else if (nextEle && isAbove(nextEle, draggingEle)) {
        swap(nextEle, placeholder);
    }
};

const mouseUpHandler = function () {
    if (placeholder && draggingEle) {
        placeholder.parentNode.insertBefore(draggingEle, placeholder);
        placeholder.parentNode.removeChild(placeholder);
        draggingEle.classList.remove('dragging');
        draggingEle.style.removeProperty('top');
        draggingEle.style.removeProperty('left');
        draggingEle.style.removeProperty('position');

        const items = document.querySelectorAll('.draggable');
        const order = Array.from(items).map((item, index) => ({
            id: item.dataset.id,
            priority: index
        }));

        fetch('/update-priority/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({order})
        });
    }

    document.removeEventListener('mousemove', mouseMoveHandler);
    document.removeEventListener('mouseup', mouseUpHandler);
};

function isAbove(nodeA, nodeB) {
    const rectA = nodeA.getBoundingClientRect();
    const rectB = nodeB.getBoundingClientRect();
    return rectA.top < rectB.top;
}

function swap(nodeA, nodeB) {
    const parent = nodeA.parentNode;
    parent.insertBefore(nodeA, nodeB);
}

document.querySelectorAll('.draggable').forEach(item => {
    item.addEventListener('mousedown', mouseDownHandler);
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (const cookie of cookies) {
            const trimmed = cookie.trim();
            if (trimmed.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(trimmed.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
