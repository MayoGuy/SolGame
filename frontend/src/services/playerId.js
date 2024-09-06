export function getRandomId() {
    const storedId = localStorage.getItem('playerId');

    if (storedId) {
        return storedId;
    } else {
        const newId = generateRandomId();
        localStorage.setItem('playerId', newId);
        return newId;
    }
}


export function generateRandomId(length = 8) {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    for (let i = 0; i < length; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
}