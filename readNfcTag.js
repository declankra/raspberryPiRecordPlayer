const { NFC } = require('nfc-pcsc');

const nfc = new NFC(); // You can pass a logger object to see internal library logs

console.log("NFC Reader has started.");

nfc.on('reader', reader => {
    
    console.log(`${reader.reader.name} device attached`);

    reader.on('card', card => {
        console.log(`Card with UID ${card.uid} detected by ${reader.reader.name}`);
        console.log(card.uid);
        process.exit(); // Exit after the first read
    });

    reader.on('error', err => {
        console.error(`Error occurred on ${reader.reader.name}:`, err);
        process.exit(1); // Exit with error code
    });

    reader.on('end', () => {
        console.log(`${reader.reader.name} device removed`);
    });
    
});

nfc.on('error', err => {
    console.error('An error occurred with NFC Reader:', err);
    process.exit(1); // Exit with error code
});
