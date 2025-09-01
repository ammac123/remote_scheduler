(() => {
const pad0 = (n) => (n < 0 ? 0 : n);

function breakdown(ms){
    const total = Math.max(0, ms);
    const d = Math.floor(total / (1000 * 60 * 60 * 24));
    const h = Math.floor((total % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const m = Math.floor((total % (1000 * 60 * 60)) / (1000 * 60));
    const s = Math.floor((total % (1000 * 60)) / (1000));

    return {d,h,m,s}
}

function setValue(el, value) {
    if (el) el.style.setProperty('--value', pad0(value));
}

function renderWidget(widget, nowTs) {
    const targetStr = widget.dataset.target;
    if (!targetStr) return;

    const targetTs = new Date(targetStr).getTime();
    if (Number.isNaN(targetTs)) {
        widget.setAttribute('aria-label', 0);
        return;
    }
    
    const remaining = targetTs - nowTs;
    if (remaining <= 0) {
        ['days', 'hours', 'minutes', 'seconds'].forEach(part=> {
            const el = widget.querySelector(`[data-part="${part}"]`);
            if (el) setValue(el, 0);
        });
    widget.dataset.done = "true";
    return;
    }

    const { d,m,h,s } = breakdown(remaining);
    
    setValue(widget.querySelector('[data-part="days"]'), d);
    setValue(widget.querySelector('[data-part="hours"]'), h);
    setValue(widget.querySelector('[data-part="minutes"]'), m);
    setValue(widget.querySelector('[data-part="seconds"]'), s);
}

const registry = new Set();

function initWidgets(widget) {
    if (widget.dataset.initialised) return;
    widget.dataset.initialised = "true";
    registry.add(widget);
    renderWidget(widget, Date.now());
}


function initAll() {
    document.querySelectorAll('.countdown-widget[data-target]').forEach(initWidgets);
}

function tick() {
    const now = Date.now();
    registry.forEach(w => {
        if (w.dataset.done === "true") return;
        renderWidget(w, now);
    });
}

function startTicker(){
    const ms = 100 - (Date.now() % 100);
    setTimeout(() => {
        tick();
        setInterval(tick, 100);
    }, ms);
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {initAll(); startTicker(); });
} else {
    initAll(); startTicker();
}

})();