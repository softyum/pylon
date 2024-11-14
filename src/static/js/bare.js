/**
 * How Debouncing Works
 * Debouncing works by setting a timer that delays the execution of the function. 
 * If another event occurs before the timer completes, the timer is reset. 
 * Only when the timer completes without interruption does the function execute.
 * 
 * // Usage
 * const handleResize = debounce(() => {
 *  console.log('Window resized');
 * }, 300);
 * window.addEventListener('resize', handleResize);
 */
function debounce(func, delay = 500) {
    let timeoutId;
    return function (...args) {
        const context = this;
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(context, args), delay);
    };
}

function debounce_wand(delay = 500) {
    let timeoutId;
    return function (func) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(func, delay);
    };
}

function throttle_stream(delay = 500) {
    const magic = {};
    return function (url, gulpChunk, initRead) {
        if (magic.inThrottle) return;
        magic.inThrottle = true;

        if (magic.controller) {
            magic.controller.abort();
            console.log("Download aborted");
        }

        magic.controller = new AbortController();
        setTimeout(() => magic.inThrottle = false, delay);
        // signal: AbortSignal.timeout(60000),
        download_stream(url, magic.controller.signal, gulpChunk, initRead);
    }
}

function throttle_wand(limit = 500) {
    let inThrottle;
    return function (func) {
        if (!inThrottle) {
            func();
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

/**
 * How Throttling Works
 * Throttling works by allowing the function to execute immediately and 
 * then blocking subsequent calls until a specified time has passed.} func 
 * // Usage
 * const handleScroll = throttle(() => {
 *  console.log('Scrolled');
 * }, 1000);
 * window.addEventListener('scroll', handleScroll);
*/
function throttle(func, limit = 500) {
    let inThrottle;
    return function (...args) {
        if (!inThrottle) {
            const context = this;
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}


/**
 * read stream by fetch
 * fnGetURL, fnInitRead, fnReadChunk
 */
async function download_stream(url, signal, gulpChunk, initRead) {
    // signal: AbortSignal.timeout(60000),
    if (typeof initRead === "function") initRead();
    let ingestChunk;
    if (typeof gulpChunk === "function") {
        ingestChunk = gulpChunk;
    }
    else {
        ingestChunk = (chunk) => { console.log(chunk); }
    }

    const response = await fetch(url, { signal });
    if (!response.ok) {
        throw new Error(`Failed to fetch data: ${response.status}`);
    }
    try {
        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");

        while (true) {
            const { done, value } = await reader.read();
            if (done) {
                console.log("Stream complete"); break;
            }
            let chunk = decoder.decode(value)
            ingestChunk(chunk);
        }
    }
    catch (err) {
        console.warn(`Download error: ${err.message}`);
    }
}

function fetch_stream(ensureURL, gulpChunk, limit = 500) {
    let controller;
    let inThrottle;
    return async function (...args) {
        if (inThrottle) return;
        inThrottle = true;

        if (controller) {
            controller.abort();
            console.log("Download aborted");
        }

        let url = ensureURL(args);
        controller = new AbortController();
        setTimeout(() => inThrottle = false, limit);

        // signal: AbortSignal.timeout(60000),
        download_stream(url, controller.signal, gulpChunk);
    };
}
