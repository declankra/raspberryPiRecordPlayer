const { NFC } = require('nfc-pcsc');

const nfc = new NFC();

// Track current card to detect removal
let currentCard = null;

console.error('[NFC] Starting persistent NFC reader...');

nfc.on('reader', reader => {
    console.error(`[NFC] Reader attached: ${reader.reader.name}`);

    reader.on('card', card => {
        currentCard = card.uid;
        // Output format: CARD:<uid>
        console.log(`CARD:${card.uid}`);
    });

    reader.on('card.off', card => {
        currentCard = null;
        // Output when card is removed
        console.log('CARD_REMOVED');
    });

    reader.on('error', err => {
        console.error(`[NFC] Reader error: ${err.message}`);
        // Don't exit - try to recover
    });

    reader.on('end', () => {
        console.error(`[NFC] Reader removed: ${reader.reader.name}`);
        // Don't exit - wait for reader to be reconnected
    });
});

nfc.on('error', err => {
    console.error(`[NFC] NFC error: ${err.message}`);
    // Don't exit on errors - try to keep running
});

// Keep process alive and handle graceful shutdown
process.on('SIGTERM', () => {
    console.error('[NFC] Received SIGTERM, shutting down...');
    process.exit(0);
});

process.on('SIGINT', () => {
    console.error('[NFC] Received SIGINT, shutting down...');
    process.exit(0);
});

// Heartbeat to stderr every 30 seconds (for debugging)
setInterval(() => {
    console.error(`[NFC] Heartbeat - current card: ${currentCard || 'none'}`);
}, 30000);
