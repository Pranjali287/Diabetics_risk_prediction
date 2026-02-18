function formatDate(date) {
    return date.toISOString().split('T')[0];
}

function logMessage(message) {
    console.log(`[${formatDate(new Date())}] ${message}`);
}

function deepClone(obj) {
    return JSON.parse(JSON.stringify(obj));
}

export { formatDate, logMessage, deepClone };