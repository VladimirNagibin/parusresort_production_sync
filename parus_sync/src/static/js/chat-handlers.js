// ========== 1. Скрытие оригинальных кнопок виджетов ==========
(function() {
    var style = document.createElement('style');
    style.innerHTML = `
        #jvLabelWrap {
            display: none !important;
            visibility: hidden !important;
        }
        .b24-widget-button-wrapper {
            position: absolute !important;
            top: -9999px !important;
            left: -9999px !important;
            opacity: 0 !important;
            width: 0 !important;
            height: 0 !important;
            overflow: hidden !important;
        }
    `;
    document.head.appendChild(style);

    setInterval(function() {
        var bxBtn = document.querySelector('.b24-widget-button-wrapper');
        if (bxBtn && !bxBtn.classList.contains('force-visible')) {
            bxBtn.style.position = 'absolute';
            bxBtn.style.top = '-9999px';
            bxBtn.style.left = '-9999px';
            bxBtn.style.width = '0';
            bxBtn.style.height = '0';
        }
    }, 500);
})();

// ========== 2. Логика работы unified-кнопки и чатов ==========
// Делаем функции глобальными, чтобы их могли вызывать onclick-атрибуты
window.toggleChatMenu = function() {
    var menu = document.getElementById('chatMenu');
    var isMenuOpen = menu.classList.contains('active');
    var chatClosed = false;

    // Закрыть Jivo, если открыт
    var jivoContainer = document.getElementById('jivo_action');
    if (jivoContainer && window.getComputedStyle(jivoContainer).display !== 'none') {
        if (typeof jivo_api !== 'undefined' && jivo_api.close) {
            jivo_api.close();
        } else {
            var jivoCloseBtn = document.getElementById('jivo_close_button');
            if (jivoCloseBtn) jivoCloseBtn.click();
        }
        if (isMenuOpen) menu.classList.remove('active');
        chatClosed = true;
    }

    // Закрыть Битрикс, если открыт
    var bxShadow = document.querySelector('.b24-widget-button-shadow');
    if (bxShadow && window.getComputedStyle(bxShadow).visibility === 'visible') {
        bxShadow.click();
        var escEvent = new KeyboardEvent('keydown', { key: 'Escape', code: 'Escape', keyCode: 27, which: 27, bubbles: true });
        window.dispatchEvent(escEvent);
        if (isMenuOpen) menu.classList.remove('active');
        chatClosed = true;
    }

    // Если ни один чат не был открыт – переключаем меню
    if (!chatClosed) {
        isMenuOpen ? menu.classList.remove('active') : menu.classList.add('active');
    }
};

window.openJivo = function() {
    document.getElementById('chatMenu').classList.remove('active');
    if (typeof jivo_api !== 'undefined' && jivo_api.open) {
        jivo_api.open();
    } else {
        alert('Jivo загружается...');
    }
};

window.openBitrix = function() {
    document.getElementById('chatMenu').classList.remove('active');
    var bxWrapper = document.querySelector('.b24-widget-button-wrapper');
    if (bxWrapper) {
        var oldStyle = bxWrapper.getAttribute('style');
        var bxInnerBtn = bxWrapper.querySelector('.b24-widget-button-block');
        var oldInnerStyle = bxInnerBtn ? bxInnerBtn.getAttribute('style') : '';

        bxWrapper.classList.add('force-visible');
        bxWrapper.style.cssText = "position: fixed !important; top: 0 !important; left: 0 !important; width: 50px !important; height: 50px !important; opacity: 0 !important; z-index: 999999 !important; visibility: visible !important; pointer-events: auto !important;";
        if (bxInnerBtn) {
            bxInnerBtn.style.pointerEvents = 'auto';
            bxInnerBtn.style.visibility = 'visible';
            bxInnerBtn.style.opacity = '0';
            bxInnerBtn.click();
        } else {
            bxWrapper.click();
        }
        setTimeout(function() {
            bxWrapper.classList.remove('force-visible');
            bxWrapper.setAttribute('style', oldStyle);
            if (bxInnerBtn) bxInnerBtn.setAttribute('style', oldInnerStyle);
        }, 200);
    } else {
        alert('Виджет Битрикс еще не загрузился.');
    }
};

// Закрывать меню при клике вне его
document.addEventListener('click', function(e) {
    var menu = document.getElementById('chatMenu');
    var btn = document.querySelector('.unified-chat-btn');
    if (menu && btn && !menu.contains(e.target) && !btn.contains(e.target)) {
        menu.classList.remove('active');
    }
});
